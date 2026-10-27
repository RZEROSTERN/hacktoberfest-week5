"""Render measured results and an explicit raw-output audit into BENCHMARKS.md."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
Json = dict[str, Any]


def seconds(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.2f}"


def pair(values: Json) -> str:
    return f"{seconds(values['p50'])} / {seconds(values['p95'])}"


def main() -> None:
    result_path = ROOT / "spike/results/mac-m2-pro-16gb.json"
    results: Json = json.loads(result_path.read_text(encoding="utf-8"))
    audit: Json = json.loads((ROOT / "spike/audit.json").read_text(encoding="utf-8"))
    reviewed = set(audit["reviewed_attempts"])
    issues = {item["key"]: item for item in audit["issues"]}
    text = [
        "# Local model benchmark",
        "",
        "## Decision",
        "",
        "**No default selected.** The required Gemma 4 comparison exceeds the engine memory",
        "budget on this Mac. Development stops before the model-spike PR, as required",
        "by step 4 of docs/PROJECT_BRIEF.md. No target has been silently relaxed.",
        "",
        "## Setup",
        "",
        f"- Run: {results['created_at']}; label {results['label']}.",
        f"- OS/architecture: {results['platform']} / {results['architecture']}.",
        f"- Installed RAM: {results['total_ram_bytes'] / 1024**3:.1f} GiB.",
        f"- Bundled engine: {results['engine_version']}; dedicated loopback port, own home/models.",
        "- Background priority, one model, one request; "
        "other desktop applications were not closed.",
        "- Both sets use 120 fixed cases: 20 per object, 10 per language per object.",
        "- Temperature 0, seed 42, context 4096, output cap 128, thinking off.",
        "- One regeneration after an invalid voice reply, then an authored fallback.",
        "- This is one run per model, not a hardware-independent performance guarantee.",
        "",
        "The model tags were checked in the [official Ollama catalog](https://ollama.com/library/gemma4/tags).",
        "The local GGUF manifests resolve to the specific digests below; moving aliases",
        "may resolve differently on a future run. Copied blobs were SHA-256 verified.",
        "",
        "| Model | Digest | Cases |",
        "| --- | --- | ---: |",
    ]
    for model in results["models"]:
        text.append(
            f"| {model['model']} | `{model['installed']['digest']}` | {len(model['rows'])} |"
        )
    text += [
        "",
        "## Warm timing and classification",
        "",
        "Times are seconds, shown as **p50 / p95**. The first case per model is cold",
        "and is excluded from warm statistics. Percentiles use the lower observed sample",
        "at floor((n-1)*p), without interpolation. Raw first fragment is typically JSON",
        "syntax; the validated display boundary waits for the accepted reply or fallback.",
        "",
        "| Model | Raw TTFT | Raw full reply | "
        "Validated display / pipeline | Accuracy | Fallbacks |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in results["models"]:
        summary = model["summary"]
        text.append(
            f"| {model['model']} | {pair(summary['warm_raw_ttft_s'])} | "
            f"{pair(summary['warm_raw_full_s'])} | {pair(summary['warm_pipeline_s'])} | "
            f"{100 * summary['accuracy']:.1f}% | {summary['fallbacks']}/{summary['cases']} |"
        )
    text += [
        "",
        "Targets from the brief: first token <2 s, full reply <6 s, classification",
        "accuracy >=85%. Raw model latency and actual validated-display delay are",
        "reported separately; cosmetic typewriter animation is not included.",
        "",
        "| Model | Cold raw TTFT | Cold full reply | "
        "Cold validated display | Warm pipeline maximum |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for model in results["models"]:
        summary = model["summary"]
        cold = summary["cold"]
        text.append(
            f"| {model['model']} | {seconds(cold['raw_first_token_s'])} | "
            f"{seconds(cold['raw_full_reply_s'])} | {seconds(cold['pipeline_s'])} | "
            f"{seconds(summary['warm_pipeline_s']['max'])} |"
        )
    text += [
        "",
        "## Peak engine memory",
        "",
        "GB here means 1,000,000,000 bytes. The engine target is <=3 GB, leaving",
        "room for the rest of the game within its <=4 GB total budget.",
        "",
        "| Model | Tree RSS GB | macOS physical footprint GB | Ollama reported size GB | Budget |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for model in results["models"]:
        summary = model["summary"]
        text.append(
            f"| {model['model']} | {summary['peak_tree_rss_bytes'] / 1e9:.2f} | "
            f"{summary['peak_tree_physical_footprint_bytes'] / 1e9:.2f} | "
            f"{summary['peak_ollama_size_bytes'] / 1e9:.2f} | "
            f"{'Pass' if summary['meets_memory_target'] else 'Fail'} |"
        )
    text += [
        "",
        "The sampler includes the dedicated Ollama server and all descendants, including",
        "llama-server, at 100 ms intervals. macOS physical footprint comes from the",
        "public proc_pid_rusage/rusage_info_v2 interface in Apple’s installed SDK.",
        "It captures costs that RSS alone does not adequately represent for this run.",
        "Ollama’s own size report was much smaller than the measured process cost.",
        "Using only RSS or only /api/ps would give a misleading memory result.",
        "The full Electron/game process budget has not been measured yet.",
        "",
        "## Canon and voice audit",
        "",
        "The rule-based prototype is not connected to any player-facing endpoint.",
        "Passing a schema and checking allowed names/years cannot prove arbitrary",
        "sentences true. All raw synthetic replies are retained for inspection.",
        "",
        f"Audit: {audit['reviewer']}.",
        "",
        "| Model | Reviewed / generated attempts | Flagged canon issues | "
        "Blocked | Escaped | False rejections |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in results["models"]:
        generated: list[tuple[str, Json]] = [
            (f"{model['model']}/{row['id']}/{index}", attempt)
            for row in model["rows"]
            for index, attempt in enumerate(row["attempts"])
            if "proposal" in attempt
        ]
        canon = [
            (key, item)
            for key, item in generated
            if issues.get(key, {}).get("canon_issue")
        ]
        blocked = sum(bool(item.get("reasons")) for _, item in canon)
        false_positive = sum(
            bool(issues.get(key, {}).get("validator_false_positive"))
            for key, _ in generated
        )
        text.append(
            f"| {model['model']} | "
            f"{sum(key in reviewed for key, _ in generated)}/{len(generated)} | "
            f"{len(canon)} ({100 * len(canon) / len(generated):.1f}%) | "
            f"{blocked} | {len(canon) - blocked} | {false_positive} |"
        )
    text += ["", "### Voice observations", ""]
    for model, note in audit.get("model_voice_notes", {}).items():
        text.append(f"- **{model}:** {note}")
    validation = results["validator"]
    text += [
        "",
        f"The final validator catches **{validation['caught']}/"
        f"{validation['contradictions']}** injected",
        f"false statements and rejects **{validation['false_rejections']}/"
        f"{validation['good_controls']}** authored controls.",
        "That finite mutation suite is separate from the raw-output audit. It is not",
        "a universal 100% canon-safety claim, and uncovered free-text issues still fail",
        "the requirement that every contradiction be caught before display.",
        "",
        "### Recorded issues",
        "",
    ]
    for issue in audit["issues"]:
        kind = "Canon" if issue.get("canon_issue") else "Voice"
        if issue.get("validator_false_positive"):
            kind = "False rejection"
        text.append(f"- **{issue['key']} ({kind}):** {issue['note']}")
    text += [
        "",
        "## Breakdown",
        "",
        "| Model / subset | Correct | Total | Accuracy |",
        "| --- | ---: | ---: | ---: |",
    ]
    for model in results["models"]:
        groups: dict[str, list[Json]] = defaultdict(list)
        for row in model["rows"]:
            for key in [row["language"], row["kind"], row["object_id"]]:
                groups[key].append(row)
        for name, rows in groups.items():
            count = sum(row["classification_correct"] for row in rows)
            text.append(
                f"| {model['model']} / {name} | {count} | {len(rows)} | "
                f"{100 * count / len(rows):.1f}% |"
            )
    text += [
        "",
        "## Calibration and limits",
        "",
        "- A two-case pilot established transport and timing, but covered only locked contexts.",
        "- The initial full run was interrupted when recovered contexts exposed invented fact IDs.",
        "  Its partial evidence is preserved as calibration-before-fact-id-enum.*.",
        "- The schema now restricts fact IDs to the visible set, with no IDs allowed when locked.",
        "  A four-case locked/recovered pilot verified the fix before the complete restart.",
        "- Initial rule checks missed six negated/impossible-life statements; those forms were",
        "  addressed before the final run. The final mutation suite remains finite and synthetic.",
        "- CPU/GPU contention, model load, compression and paging can affect latency.",
        "  This run used the normal development desktop; "
        "it does not establish an idle-Mac best case.",
        "- Windows and Linux Mint have not been benchmarked. The runner supports both,",
        "  but actual hardware and graphics-memory accounting still need their own run.",
        "- The local API contract is unchanged: no inference endpoint is shipped by this spike.",
        "",
        "## Options requiring owner direction",
        "",
        "1. **Keep the budgets and compare smaller local models (recommended).**",
        "   [Gemma 3 1B](https://ollama.com/library/gemma3:1b) is listed at 806 MB,",
        "   and [Qwen 3.5 0.8B](https://ollama.com/library/qwen3.5:0.8b) at roughly 1.2–1.3 GB.",
        "   Download sizes are not runtime RAM guarantees; "
        "both need this same quality/safety benchmark.",
        "   No additional model is downloaded or selected here.",
        "2. **Investigate a text-only/lower-quantized Gemma 4 variant.** This may remove",
        "   unused multimodal cost, but requires a separate "
        "compatibility, memory and quality spike.",
        "   It has not been measured and is not assumed to fit.",
        "3. **Revise the memory/latency requirements for Gemma 4.** This changes the original",
        "   modest-hardware promise and would still require fixing escaped canon issues.",
        "",
        "The recommended next step keeps the original offline and <=4 GB product goals.",
        "Every option still needs a validator that rejects unsupported free-text claims.",
        "",
        "## Evidence and reproduction",
        "",
        "- spike/results/mac-m2-pro-16gb.json and .ndjson: complete measured final run.",
        "- spike/results/run-source-sha256.json: exact source/input hashes used.",
        "- spike/audit.json: reviewed raw-attempt IDs and qualitative findings.",
        "- spike/cases.json and validator_cases.json: fixed labels and challenge controls.",
        "- spike/README.md: commands and measurement details for all three machines.",
        "- api/prompts/spirit.spike.v1.txt: versioned prompt, with dynamic visible-fact schema.",
        "",
        "Only loopback calls to the dedicated bundled engine performed inference.",
        "API semantics were checked in the official Ollama documentation for",
        "[chat](https://docs.ollama.com/api/chat),",
        "[structured output](https://docs.ollama.com/capabilities/structured-outputs),",
        "[loaded models](https://docs.ollama.com/api/ps), and",
        "[unloading](https://docs.ollama.com/api/generate).",
        "",
    ]
    (ROOT / "docs/BENCHMARKS.md").write_text("\n".join(text).rstrip() + "\n")
    print("Generated docs/BENCHMARKS.md from measured results and the explicit audit.")


if __name__ == "__main__":
    main()
