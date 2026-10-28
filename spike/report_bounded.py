"""Replay every bounded output and report the original, unrelaxed spike gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "api"))

from app.dialogue import reply_choices, resolve_choice  # noqa: E402
from app.story import Story, load_story  # noqa: E402
from report import pair, seconds  # noqa: E402

Json = dict[str, Any]


def assess(
    model: Json, story: Story, validation: Json, *, prepared: bool = False
) -> Json:
    rows = model["rows"]
    mismatches = []
    for row in rows:
        obj = next(item for item in story.objects if item.id == row["object_id"])
        if row["fallback_used"]:
            state = "recovered" if obj.id in row["recovered"] else "error"
            expected = (
                f"{obj.id}.{state}",
                getattr(getattr(obj.fallbacks, state), row["language"]),
            )
        else:
            choices = reply_choices(
                story,
                obj.id,
                set(row["recovered"]),
                row["predicted_relevant"],
                row["language"],
            )
            expected = resolve_choice(row["attempts"][-1]["raw"], choices)
        if expected != (row["safe_reply_id"], row["safe_reply"]):
            mismatches.append(row["id"])
    subsets = {}
    for name in ("original", "holdout"):
        chosen = [row for row in rows if row.get("corpus", "original") == name]
        correct = sum(row["classification_correct"] for row in chosen)
        subsets[name] = {
            "correct": correct,
            "total": len(chosen),
            "accuracy": correct / len(chosen) if chosen else 0,
        }
    gates = {
        "classification": all(s["accuracy"] >= 0.85 for s in subsets.values()),
        "raw_ttft": all(
            row["raw_first_token_s"] is not None and row["raw_first_token_s"] < 2
            for row in rows
        ),
        "full_reply": all(
            row["raw_full_reply_s"] is not None and row["raw_full_reply_s"] < 6
            for row in rows
        ),
        "safe_first_text": all(row["pipeline_s"] < 2 for row in rows),
        "engine_memory": model["summary"]["conservative_peak_bytes"] <= 3_000_000_000,
        "authored_boundary": not mismatches
        and validation["caught"] == validation["contradictions"]
        and validation["false_rejections"] == 0,
        "complete": all(s["total"] == 120 for s in subsets.values()),
    }
    if prepared:
        gates["prepared_and_resident"] = bool(model.get("preparation")) and bool(
            (model.get("idle_probe") or {}).get("resident")
        )
    return {
        "model": model["model"],
        "subsets": subsets,
        "gates": gates,
        "qualified": all(gates.values()),
        "boundary_mismatches": mismatches,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared", action="store_true")
    args = parser.parse_args()
    run_name = "prepared" if args.prepared else "bounded"
    result_path = ROOT / f"spike/results/mac-m2-pro-16gb-{run_name}.json"
    results: Json = json.loads(result_path.read_text())
    story = load_story(ROOT / "content")
    for path, digest in json.loads(
        (ROOT / f"spike/results/run-source-{run_name}-sha256.json").read_text()
    ).items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != digest:
            raise ValueError(f"Measured source changed: {path}")
    assessments = [
        assess(model, story, results["validator"], prepared=args.prepared)
        for model in results["models"]
    ]
    qualified = [
        m for m, a in zip(results["models"], assessments, strict=True) if a["qualified"]
    ]
    chosen = (
        min(qualified, key=lambda m: m["summary"]["conservative_peak_bytes"])
        if qualified
        else None
    )
    audit = {
        "method": "Replay every selected ID/text against state-scoped authored content",
        "assessments": assessments,
        "selected_default": chosen["model"] if chosen else None,
        "limitation": "Output confinement is structural, not perfect semantic classification. "
        "Authored content was approved separately.",
    }
    (ROOT / f"spike/audit-{run_name}.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n"
    )
    text = ["# Local model benchmark", "", "## Decision", ""]
    if chosen:
        text.append(
            f"**Select {chosen['model']} as the recommended default.** "
            "It meets every measured gate below,"
        )
        text.append(
            (
                "after explicit pregame preparation and on the held-out corpus. "
                if args.prepared
                else "including cold latency and the held-out corpus. "
            )
            + "Runtime reads the player's local settings;"
        )
        text.append(
            "no model is loaded/downloaded until consent and selection in the first-launch wizard."
        )
    else:
        text.append(
            "**No default qualifies.** Step 4 remains stopped before its PR; "
            "see failed gates below."
        )
    text += [
        "",
        "The owner approved replacing free prose generation with authored reply selection.",
        "The local model still interprets free player messages and chooses a fitting reply.",
        "Code supplies only IDs allowed for the selected object, recovery state and relevance",
        "decision, then resolves the chosen ID to approved bilingual content. No generated",
        "words, extracted JSON substrings or model-supplied translations reach the player.",
        "",
        "The failed free-prose comparisons remain in [BENCHMARKS_GEMMA4.md](BENCHMARKS_GEMMA4.md)",
        "and [BENCHMARKS_SMALL_PROSE.md](BENCHMARKS_SMALL_PROSE.md), "
        "with raw evidence/audits.",
        "",
        "## Method",
        "",
        f"- Run: {results['created_at']}; {results['platform']}; "
        f"{results['architecture']}; engine {results['engine_version']}.",
        "- 16 GiB MacBook Pro M2 Pro; normal development desktop, one run per model.",
        "- Isolated bundled Ollama, own home/models, dynamic loopback port, low priority;",
        "  one loaded model and one inference request at a time. No cloud inference.",
        "- Unchanged 120 original cases plus 120 new bilingual cases, authored/frozen before",
        "  inference. Each corpus has 20 cases/object: 8 relevant, 6 unrelated, 6 adversarial;",
        "  10 English and 10 Spanish. New cases also exercise partially recovered states.",
        "- The classifier prompt/options are unchanged from the smaller-model comparison.",
        "  Its first validated boolean is graded. A missing/invalid result counts as wrong.",
        "- Classifier (32 tokens), then reply selector (48 tokens), at most one selector retry.",
        "  All timing includes both calls, validation and fallback. Total deadline: 6 seconds.",
        "- Context 4096, temperature 0, seed 42. Thinking omitted for Gemma 3 and disabled",
        "  where supported for Qwen. Capabilities, digests and options accompany the results.",
        (
            "- The model is prepared before player input, then retained with keep_alive=-1."
            if args.prepared
            else "- The first case is cold for a fresh model process, not an emptied OS disk cache."
        ),
        "  Warm p50/p95 use floor((n-1)*p), excluding that first case. Maxima include every case.",
        "- No prompt was tuned against the new-corpus answers. The earlier 20-case pilot covers",
        "  original cases only. An initial full start was interrupted for a lint-only import",
        "  annotation; the final complete run has a separate frozen source hash record.",
        "",
        "## Classification",
        "",
        "| Model | Original corpus | New held-out corpus | Fallbacks |",
        "| --- | ---: | ---: | ---: |",
    ]
    if args.prepared:
        text += [
            "",
            "## Startup preparation",
            "",
            "Startup is shown separately; it is not counted as a player reply or hidden",
            "with a cosmetic token. Integration must gate player input until preparation",
            "succeeds, or explicitly enter authored fallback mode. Startup memory is included",
            "in the process-tree peak. Each model stays loaded across a 35-second idle probe,",
            "longer than the previous 30-second keep-alive. The next real reply is timed too.",
            "The API helper uses Ollama's documented empty-request preload and keep_alive=-1",
            "([official FAQ](https://docs.ollama.com/faq)); explicit unload/owned-tree cleanup",
            "still runs on close. Download consent and readiness UI are later steps.",
            "The earlier cold-interaction run remains in",
            "[BENCHMARKS_BOUNDED_COLD.md](BENCHMARKS_BOUNDED_COLD.md),",
            "with source revision 7d468fe. Preparing is a startup orchestration fix, not",
            "a claim that cold model loading itself now takes less than two seconds.",
            "",
            "| Model | Cold preparation seconds | Resident after idle |",
            "| --- | ---: | --- |",
        ]
        for model in results["models"]:
            text.append(
                f"| {model['model']} | {model['preparation']['startup_s']:.2f} | "
                f"{model['idle_probe']['resident']} |"
            )
    for model, a in zip(results["models"], assessments, strict=True):
        cols = [
            f"{s['correct']}/{s['total']} ({100 * s['accuracy']:.1f}%)"
            for s in a["subsets"].values()
        ]
        text.append(
            f"| {model['model']} | {' | '.join(cols)} | {model['summary']['fallbacks']}/240 |"
        )
    text += [
        "",
        "## Latency (seconds)",
        "",
        "Warm values are **p50 / p95**. Raw TTFT is the selector's first JSON fragment,",
        "including classifier time; safe first text waits until the ID is validated and resolved.",
        "The typewriter animation is excluded. Neither metric is replaced with a cosmetic token.",
        "",
        "| Model | Warm raw TTFT | Warm full response | Warm safe first text |",
        "| --- | ---: | ---: | ---: |",
    ]
    for model in results["models"]:
        s = model["summary"]
        text.append(
            f"| {model['model']} | {pair(s['warm_raw_ttft_s'])} | "
            f"{pair(s['warm_raw_full_s'])} | {pair(s['warm_pipeline_s'])} |"
        )
    text += [
        "",
        (
            "| Model | First prepared TTFT / full / safe | Maximum TTFT / full / safe |"
            if args.prepared
            else "| Model | Cold raw TTFT / full / safe | Maximum raw TTFT / full / safe |"
        ),
        "| --- | ---: | ---: |",
    ]
    for model in results["models"]:
        s = model["summary"]
        c = s["cold"]
        text.append(
            f"| {model['model']} | {seconds(c['raw_first_token_s'])} / "
            f"{seconds(c['raw_full_reply_s'])} / {seconds(c['pipeline_s'])} | "
            f"{seconds(max(r['raw_first_token_s'] or 0 for r in model['rows']))} / "
            f"{seconds(max(r['raw_full_reply_s'] or 0 for r in model['rows']))} / "
            f"{seconds(max(r['pipeline_s'] for r in model['rows']))} |"
        )
    text += [
        "",
        "## Peak engine memory",
        "",
        "GB is decimal. Sample the dedicated engine and all descendants every 100 ms.",
        "The budget uses the largest of RSS, macOS physical footprint and Ollama allocations.",
        "macOS footprint uses the public proc_pid_rusage/rusage_info_v2 ABI. Other-platform",
        "GPU accounting and the whole Electron/game <=4 GB budget still need measurement.",
        "",
        "| Model | RSS GB | macOS footprint GB | Conservative peak GB |",
        "| --- | ---: | ---: | ---: |",
    ]
    for model in results["models"]:
        s = model["summary"]
        text.append(
            f"| {model['model']} | {s['peak_tree_rss_bytes'] / 1e9:.2f} | "
            f"{s['peak_tree_physical_footprint_bytes'] / 1e9:.2f} | "
            f"{s['conservative_peak_bytes'] / 1e9:.2f} |"
        )
    v = results["validator"]
    text += [
        "",
        "## Authored-output boundary",
        "",
        f"The live boundary rejects **{v['caught']}/{v['contradictions']}** "
        "recorded false-prose injections",
        "placed next to legal IDs across both languages and every object/state/relevance scope.",
        f"All **{v['good_controls']}** legal controls pass; "
        f"false rejections: **{v['false_rejections']}**.",
        "This checks whole-response confinement, not semantic entailment of arbitrary prose.",
        "Every selected ID/text in the real run is also replayed against its exact legal scope;",
        f"Fallbacks are checked against authored object/state text. See audit-{run_name}.json.",
        "Unit regressions reject locked/foreign IDs, extra fields, prose before/after JSON,",
        "fences and wrong types; failures exercise the single retry and authored fallback.",
        "The approved biography, scenes and fallback text have not changed.",
        "",
        "## Gate results",
        "",
        "Require >=85% accuracy separately on each corpus, every raw and safe first-text",
        "delay <2 s, every full reply <6 s, engine <=3 GB, complete data and no output",
        (
            "outside the authored boundary. Every prepared interaction and its tails are checked."
            if args.prepared
            else "outside the authored boundary. These checks include cold cases and latency tails."
        ),
        "",
        "| Model | Failed gates | Qualified |",
        "| --- | --- | --- |",
    ]
    for a in assessments:
        failed = (
            ", ".join(k for k, passed in a["gates"].items() if not passed) or "None"
        )
        text.append(f"| {a['model']} | {failed} | {a['qualified']} |")
    text += [
        "",
        "## Evidence and reproduction",
        "",
        f"- spike/config-{run_name}.json; api/prompts/relevance.spike.v3.txt "
        "and reply-selection.v1.txt.",
        "- api/app/dialogue.py is the actual interpreter exercised by spike/bounded.py.",
        f"- spike/results/mac-m2-pro-16gb-{run_name}.json/.ndjson retain every synthetic decision.",
        f"- spike/results/run-source-{run_name}-sha256.json freezes measured source/content.",
        "- spike/results/calibration-bounded-pilot.* retains the original-case pilot.",
        f"- spike/audit-{run_name}.json records replay, gates and selected default.",
        "- [spike/README.md](../spike/README.md) has the same local command for all three OSes.",
        "- Generate: uv run --project api python spike/report_bounded.py"
        + (" --prepared" if args.prepared else "")
        + ".",
        "- Windows and Linux Mint performance/installer testing remain unverified.",
        "",
        "The bounded approach sacrifices open-ended spirit prose. AI still controls semantic",
        "interpretation and selects a contextual authored response; deterministic code owns",
        "all facts, legal reply scopes, the clock, memory progression and endings.",
        "",
    ]
    output = (
        "docs/BENCHMARKS.md" if args.prepared else "docs/BENCHMARKS_BOUNDED_COLD.md"
    )
    (ROOT / output).write_text("\n".join(text).rstrip() + "\n")
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
