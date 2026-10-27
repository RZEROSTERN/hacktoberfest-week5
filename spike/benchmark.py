#!/usr/bin/env python3
"""Reproducible local-only dialogue benchmark; run through the API's uv environment."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import socket
import subprocess
import sys
import threading
import time
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "api"))

import httpx  # noqa: E402
import psutil  # noqa: E402
from app.canon_validation import validate_proposal  # noqa: E402
from app.ollama import (  # noqa: E402
    Classification,
    Proposal,
    chat,
    proposal_schema,
    thinking_control,
)
from app.story import Story, load_story  # noqa: E402
from memory import physical_footprint  # noqa: E402
from pydantic import ValidationError  # noqa: E402

Json = dict[str, Any]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class Memory:
    """Adapted from Slothshot, scoped to the owned engine PID and all descendants."""

    def __init__(self, pid: int) -> None:
        self.process = psutil.Process(pid)
        self.peak = 0
        self.case_peak = 0
        self.peak_footprint = 0
        self.case_footprint = 0
        self.errors = 0
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.loop, daemon=True)

    def sample(self) -> None:
        try:
            processes = [self.process, *self.process.children(recursive=True)]
            total = sum(
                proc.memory_info().rss for proc in processes if proc.is_running()
            )
            self.peak = max(self.peak, total)
            self.case_peak = max(self.case_peak, total)
            footprint = sum(physical_footprint(proc.pid) or 0 for proc in processes)
            self.peak_footprint = max(self.peak_footprint, footprint)
            self.case_footprint = max(self.case_footprint, footprint)
        except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
            self.errors += 1

    def loop(self) -> None:
        while not self.stop_event.wait(0.1):
            self.sample()

    def start(self) -> None:
        self.sample()
        self.thread.start()

    def stop(self) -> None:
        self.sample()
        self.stop_event.set()
        self.thread.join(timeout=2)


def stop_tree(child: subprocess.Popen[bytes]) -> None:
    try:
        processes = psutil.Process(child.pid).children(recursive=True)
        processes.append(psutil.Process(child.pid))
        for proc in processes:
            with suppress(psutil.NoSuchProcess):
                proc.terminate()
        _, remaining = psutil.wait_procs(processes, timeout=5)
        for proc in remaining:
            with suppress(psutil.NoSuchProcess):
                proc.kill()
        child.wait(timeout=5)
    except psutil.NoSuchProcess:
        pass


def engine_environment(models_dir: Path, home: Path, port: int) -> dict[str, str]:
    keys = [
        "PATH",
        "TMPDIR",
        "TEMP",
        "TMP",
        "SystemRoot",
        "SystemDrive",
        "windir",
        "COMSPEC",
        "PATHEXT",
        "LANG",
        "NUMBER_OF_PROCESSORS",
        "PROCESSOR_ARCHITECTURE",
    ]
    env = {key: os.environ[key] for key in keys if key in os.environ}
    env.update(
        HOME=str(home),
        USERPROFILE=str(home),
        OLLAMA_MODELS=str(models_dir),
        OLLAMA_HOST=f"127.0.0.1:{port}",
        OLLAMA_NO_CLOUD="1",
        OLLAMA_NOPRUNE="1",
        OLLAMA_MAX_LOADED_MODELS="1",
        OLLAMA_NUM_PARALLEL="1",
        OLLAMA_KEEP_ALIVE="30s",
    )
    return env


def unload(client: httpx.Client, model: str) -> None:
    response = client.post(
        "/api/generate", json={"model": model, "keep_alive": 0}, timeout=30
    )
    response.raise_for_status()
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if not client.get("/api/ps").json().get("models"):
            return
        time.sleep(0.2)
    raise TimeoutError("The dedicated engine did not unload the model")


def prompt(story: Story, case: Json, system: str) -> list[dict[str, str]]:
    language = case["language"]
    recovered = set(case["recovered"])
    obj = next(item for item in story.objects if item.id == case["object_id"])
    context = {
        "language": language,
        "voice": getattr(story.canon.spirit.voice, language),
        "selected_object": getattr(obj.title, language),
        "observable_description": getattr(obj.description, language),
        "connection_guidance": getattr(obj.relevance.accept, language),
        "not_a_connection": getattr(obj.relevance.reject, language),
        "visible_facts": [
            {"id": fact.id, "text": getattr(fact.text, language)}
            for fact in story.canon.facts
            if recovered.intersection(fact.revealed_by)
        ],
        "recovered_scenes": [
            {"object_id": item.id, "scene": getattr(item.memory.scene, language)}
            for item in story.objects
            if item.id in recovered
        ],
        "output_schema": proposal_schema(
            [
                fact.id
                for fact in story.canon.facts
                if recovered.intersection(fact.revealed_by)
            ]
        ),
    }
    return [
        {
            "role": "system",
            "content": system + "\n" + json.dumps(context, ensure_ascii=False),
        },
        {"role": "user", "content": case["message"]},
    ]


def run_case(
    origin: str,
    model: str,
    case: Json,
    story: Story,
    system: str,
    memory: Memory,
    config: Json,
) -> Json:
    messages = prompt(story, case, system)
    started = time.perf_counter()
    memory.case_peak = 0
    memory.case_footprint = 0
    captures: list[Json] = []
    selected: Proposal | None = None
    prediction: bool | None = None
    classification: Json | None = None
    classification_s = 0.0
    if config.get("separate_classification"):
        obj = next(item for item in story.objects if item.id == case["object_id"])
        classifier = (ROOT / config["classifier_prompt_file"]).read_text(
            encoding="utf-8"
        )
        classifier_context = {
            "object": getattr(obj.title, case["language"]),
            "description": getattr(obj.description, case["language"]),
            "relevant_topics": getattr(obj.relevance.accept, case["language"]),
            "player_message": case["message"],
        }
        classifier_messages = [
            {
                "role": "system",
                "content": classifier,
            },
            {
                "role": "user",
                "content": json.dumps(classifier_context, ensure_ascii=False),
            },
        ]
        try:
            classified = chat(
                origin,
                model,
                classifier_messages,
                visible_fact_ids=[],
                timeout_s=config["timeout_s"],
                num_ctx=config["num_ctx"],
                num_predict=32,
                think=config.get("think"),
                schema=Classification.model_json_schema(),
            )
            classification = {"raw": classified.raw, "metrics": classified.metrics}
            prediction = Classification.model_validate_json(classified.raw).relevant
        except (httpx.HTTPError, ValueError, TimeoutError) as error:
            classification = {**(classification or {}), "error": type(error).__name__}
        classification_s = time.perf_counter() - started
        classification["full_s"] = classification_s
        messages[0]["content"] += (
            "\nThe separate relevance decision is "
            + json.dumps(prediction)
            + ". Keep that value for relevant; now voice a short in-character reply."
        )
    for attempt in range(2):
        try:
            captured = chat(
                origin,
                model,
                messages,
                visible_fact_ids=[
                    fact.id
                    for fact in story.canon.facts
                    if set(case["recovered"]).intersection(fact.revealed_by)
                ],
                timeout_s=config["timeout_s"],
                num_ctx=config["num_ctx"],
                num_predict=config["num_predict"],
                think=config.get("think", False),
            )
            row: Json = {
                "raw": captured.raw,
                "first_token_s": captured.first_token_s,
                "full_s": captured.full_s,
                "metrics": captured.metrics,
            }
            try:
                proposed = Proposal.model_validate_json(captured.raw)
                if prediction is None and not config.get("separate_classification"):
                    prediction = proposed.relevant
                row["proposal"] = proposed.model_dump()
                row["reasons"] = validate_proposal(
                    story, proposed, set(case["recovered"])
                )
                if not row["reasons"]:
                    selected = proposed
            except ValidationError:
                row["reasons"] = ["invalid_response_schema"]
            captures.append(row)
            if selected is not None:
                break
            if attempt == 0:
                messages.append({"role": "assistant", "content": captured.raw})
                messages.append(
                    {
                        "role": "user",
                        "content": "Your reply failed validation: "
                        + ", ".join(row["reasons"])
                        + ". Return one corrected JSON response. "
                        "Use only visible facts; do not change canon.",
                    }
                )
        except (httpx.HTTPError, ValueError, TimeoutError) as error:
            captures.append(
                {"error": type(error).__name__, "reasons": ["generation_failed"]}
            )
            break
    pipeline_s = time.perf_counter() - started
    obj = next(item for item in story.objects if item.id == case["object_id"])
    fallback_state = "recovered" if obj.id in case["recovered"] else "error"
    safe_reply = (
        selected.reply
        if selected
        else getattr(getattr(obj.fallbacks, fallback_state), case["language"])
    )
    return {
        **case,
        "predicted_relevant": prediction,
        "classification": classification,
        "classification_correct": prediction is case["expected_relevant"],
        "attempts": captures,
        "fallback_used": selected is None,
        "safe_reply": safe_reply,
        "raw_first_token_s": (
            classification_s + captures[0]["first_token_s"]
            if captures[0].get("first_token_s") is not None
            else None
        ),
        "raw_full_reply_s": (
            classification_s + captures[0]["full_s"]
            if captures[0].get("full_s") is not None
            else None
        ),
        "validated_first_token_s": pipeline_s,
        "pipeline_s": pipeline_s,
        "peak_tree_rss_bytes": memory.case_peak,
        "peak_tree_physical_footprint_bytes": memory.case_footprint,
    }


def quantile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    values = sorted(values)
    return values[min(len(values) - 1, int((len(values) - 1) * fraction))]


def stats(values: list[float]) -> Json:
    return {
        "p50": quantile(values, 0.5),
        "p95": quantile(values, 0.95),
        "max": max(values) if values else None,
    }


def validator_report(story: Story, fixture: str) -> Json:
    rows: list[Json] = []
    for case in read_json(ROOT / fixture):
        proposal = Proposal(relevant=False, reply=case["reply"], fact_ids=[])
        reasons = validate_proposal(story, proposal, set(case["recovered"]))
        rows.append({**case, "reasons": reasons, "accepted": not reasons})
    unsafe = [row for row in rows if not row["allowed"]]
    controls = [row for row in rows if row["allowed"]]
    return {
        "rows": rows,
        "contradictions": len(unsafe),
        "caught": sum(not row["accepted"] for row in unsafe),
        "good_controls": len(controls),
        "false_rejections": sum(not row["accepted"] for row in controls),
    }


def summarize(
    rows: list[Json], memory: Memory, allocations: list[Json], validation: Json
) -> Json:
    warm = rows[1:]
    result: Json = {
        "cases": len(rows),
        "accuracy": sum(row["classification_correct"] for row in rows) / len(rows),
        "fallbacks": sum(row["fallback_used"] for row in rows),
        "cold": {
            key: rows[0][key]
            for key in ["raw_first_token_s", "raw_full_reply_s", "pipeline_s"]
        },
        "warm_raw_ttft_s": stats(
            [
                row["raw_first_token_s"]
                for row in warm
                if row["raw_first_token_s"] is not None
            ]
        ),
        "warm_raw_full_s": stats(
            [
                row["raw_full_reply_s"]
                for row in warm
                if row["raw_full_reply_s"] is not None
            ]
        ),
        "warm_validated_ttft_s": stats(
            [row["validated_first_token_s"] for row in warm]
        ),
        "warm_pipeline_s": stats([row["pipeline_s"] for row in warm]),
        "peak_tree_rss_bytes": memory.peak,
        "peak_tree_physical_footprint_bytes": memory.peak_footprint,
        "memory_sample_errors": memory.errors,
        "peak_ollama_size_bytes": max(
            (row.get("size", 0) for row in allocations), default=0
        ),
        "peak_ollama_vram_bytes": max(
            (row.get("size_vram", 0) for row in allocations), default=0
        ),
        "validator_challenge_caught": validation["caught"],
        "validator_challenge_total": validation["contradictions"],
        "validator_good_false_rejections": validation["false_rejections"],
    }
    result["conservative_peak_bytes"] = max(
        result["peak_tree_rss_bytes"],
        result["peak_tree_physical_footprint_bytes"],
        result["peak_ollama_size_bytes"],
        result["peak_ollama_vram_bytes"],
    )
    result["meets_memory_target"] = result["conservative_peak_bytes"] <= 3_000_000_000
    result["meets_accuracy_target"] = result["accuracy"] >= 0.85
    result["meets_validator_challenge_target"] = (
        validation["caught"] == validation["contradictions"]
    )
    result["manual_raw_output_audit"] = (
        "pending; rules cannot certify semantic correctness"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-download",
        action="store_true",
        help="explicit consent to downloading missing weights into isolated storage",
    )
    parser.add_argument(
        "--models", nargs="+", help="override model tags in spike/config.json"
    )
    parser.add_argument("--models-dir", type=Path, default=ROOT / ".dev/spike-models")
    parser.add_argument("--ollama-binary", type=Path)
    parser.add_argument(
        "--limit", type=int, help="pilot only; never qualifies as the complete spike"
    )
    parser.add_argument("--label", default=f"{sys.platform}-{platform.machine()}")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--config", type=Path, default=ROOT / "spike/config.json")
    args = parser.parse_args()
    config = read_json(args.config)
    models = args.models or config["models"]
    suffix = ".exe" if sys.platform == "win32" else ""
    binary = args.ollama_binary or ROOT / "desktop/build/ollama" / (
        "bin/ollama" if sys.platform == "linux" else f"ollama{suffix}"
    )
    if not binary.is_file():
        parser.error(
            "Bundled Ollama is missing. Run node scripts/fetch-ollama.mjs first."
        )
    args.models_dir.mkdir(parents=True, exist_ok=True)
    work = ROOT / ".dev/spike-engine"
    home = work / "home"
    home.mkdir(parents=True, exist_ok=True)
    port = free_port()
    origin = f"http://127.0.0.1:{port}"
    path = (
        args.output
        or ROOT
        / "spike/results"
        / f"{args.label}-{datetime.now(UTC):%Y%m%dT%H%M%SZ}.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    story = load_story(ROOT / "content")
    if story.canon.review_status != "approved":
        parser.error("The story must be approved before benchmarking.")
    cases: list[Json] = read_json(ROOT / "spike/cases.json")
    if args.limit:
        cases = cases[: args.limit]
    prompt_file = config.get("prompt_file", "api/prompts/spirit.spike.v1.txt")
    system = (ROOT / prompt_file).read_text(encoding="utf-8")
    fixture = config.get("validator_fixture", "spike/validator_cases.json")
    validation = validator_report(story, fixture)
    report: Json = {
        "created_at": datetime.now(UTC).isoformat(),
        "label": args.label,
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "total_ram_bytes": psutil.virtual_memory().total,
        "config": config,
        "prompt_file": prompt_file,
        "input_sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in [
                "spike/cases.json",
                fixture,
                prompt_file,
                "api/app/canon_validation.py",
                "api/app/ollama.py",
                "spike/benchmark.py",
                "content/canon.json",
                "content/objects.json",
                "content/lines.json",
                "content/endings.json",
                *(
                    [config["classifier_prompt_file"]]
                    if config.get("separate_classification")
                    else []
                ),
            ]
        },
        "validator": validation,
        "models": [],
    }
    with (work / "engine.log").open("wb") as log:
        flags = (
            getattr(subprocess, "CREATE_NO_WINDOW", 0) if sys.platform == "win32" else 0
        )
        child = subprocess.Popen(
            [str(binary.resolve()), "serve"],
            env=engine_environment(args.models_dir.resolve(), home, port),
            stdout=log,
            stderr=log,
            creationflags=flags,
        )
        try:
            owned = psutil.Process(child.pid)
            with suppress(psutil.AccessDenied, OSError):
                owned.nice(
                    getattr(psutil, "BELOW_NORMAL_PRIORITY_CLASS", 10)
                    if sys.platform == "win32"
                    else 10
                )
            with httpx.Client(base_url=origin, timeout=10, trust_env=False) as client:
                deadline = time.monotonic() + 60
                while True:
                    if child.poll() is not None:
                        raise RuntimeError(
                            "Bundled Ollama exited; see .dev/spike-engine/engine.log"
                        )
                    try:
                        if client.get("/api/tags").is_success:
                            break
                    except httpx.HTTPError:
                        pass
                    if time.monotonic() > deadline:
                        raise TimeoutError("Bundled Ollama did not become ready")
                    time.sleep(0.2)
                version_dir = (
                    binary.parent.parent if sys.platform == "linux" else binary.parent
                )
                version_file = version_dir / "VERSION"
                report["engine_version"] = (
                    version_file.read_text().strip()
                    if version_file.exists()
                    else "unknown"
                )
                for model in models:
                    installed = client.get("/api/tags").json()["models"]
                    entry = next(
                        (item for item in installed if item["name"] == model), None
                    )
                    if entry is None and args.allow_download:
                        with client.stream(
                            "POST", "/api/pull", json={"model": model}, timeout=600
                        ) as pull:
                            pull.raise_for_status()
                            for line in pull.iter_lines():
                                if line.strip() and json.loads(line).get("error"):
                                    raise RuntimeError("Model download failed")
                        installed = client.get("/api/tags").json()["models"]
                        entry = next(
                            (item for item in installed if item["name"] == model), None
                        )
                    if entry is None:
                        raise RuntimeError(
                            f"{model} is not installed in the isolated models folder; "
                            "use --allow-download to explicitly consent to downloading it"
                        )
                    shown = client.post("/api/show", json={"model": model})
                    shown.raise_for_status()
                    if shown.json().get("remote_host") or "cloud" in model.casefold():
                        raise ValueError("Remote models are not permitted")
                    model_config = {**config, "think": thinking_control(shown.json())}
                    unload(client, model)
                    meter = Memory(child.pid)
                    meter.start()
                    rows: list[Json] = []
                    allocations: list[Json] = []
                    try:
                        for index, case in enumerate(cases):
                            row = run_case(
                                origin, model, case, story, system, meter, model_config
                            )
                            rows.append(row)
                            allocations.extend(
                                client.get("/api/ps").json().get("models", [])
                            )
                            with path.with_suffix(".ndjson").open(
                                "a", encoding="utf-8"
                            ) as progress:
                                progress.write(
                                    json.dumps(
                                        {"model": model, **row}, ensure_ascii=False
                                    )
                                    + "\n"
                                )
                            print(
                                f"{model} {index + 1}/{len(cases)} {case['id']} "
                                f"correct={row['classification_correct']} "
                                f"pipeline={row['pipeline_s']:.2f}s "
                                f"fallback={row['fallback_used']}",
                                flush=True,
                            )
                    finally:
                        meter.stop()
                        unload(client, model)
                    report["models"].append(
                        {
                            "model": model,
                            "installed": entry,
                            "run_config": model_config,
                            "capabilities": shown.json().get("capabilities", []),
                            "summary": summarize(rows, meter, allocations, validation),
                            "rows": rows,
                        }
                    )
                    path.write_text(
                        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
                    print(
                        json.dumps(
                            {"model": model, "summary": report["models"][-1]["summary"]}
                        ),
                        flush=True,
                    )
        finally:
            stop_tree(child)
            path.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    print(f"Results: {path}", flush=True)


if __name__ == "__main__":
    main()
