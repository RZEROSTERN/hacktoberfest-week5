"""Render the approved smaller-model follow-up, preserving the Gemma 4 evidence."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from report import pair, seconds

ROOT = Path(__file__).resolve().parents[1]
Json = dict[str, Any]


def main() -> None:
    results: Json = json.loads(
        (ROOT / "spike/results/mac-m2-pro-16gb-small.json").read_text()
    )
    audit: Json = json.loads((ROOT / "spike/audit-small.json").read_text())
    reviewed = set(audit["reviewed_attempts"])
    issues = {issue["key"]: issue for issue in audit["issues"]}
    text = [
        "# Local model benchmark",
        "",
        "## Smaller-model follow-up",
        "",
        audit["decision"],
        "",
        "The owner approved comparing Gemma 3 1B and Qwen 3.5 0.8B after the",
        "required Gemma 4 models exceeded the memory ceiling. The complete original",
        "report remains in [BENCHMARKS_GEMMA4.md](BENCHMARKS_GEMMA4.md), including",
        "the original 242-candidate audit. The new run does not replace that evidence.",
        "",
        "## Setup and method",
        "",
        f"- Run: {results['created_at']}; label {results['label']}.",
        f"- Platform: {results['platform']} / {results['architecture']}.",
        f"- RAM: {results['total_ram_bytes'] / 1024**3:.1f} GiB; "
        f"engine {results['engine_version']}.",
        "- Same fixed 120 cases per model: 20 per object, eight relevant, six unrelated,",
        "  six adversarial; ten English and ten Spanish per object. Labels are unchanged.",
        "- Dedicated loopback engine, isolated home and weights, low process priority,",
        "  one model and one request at a time. No cloud inference or system engine.",
        "- Context 4096, temperature 0, seed 42; 32-token classifier, 128-token voice.",
        "- Two sequential calls: relevance first, then a short spirit reply. The first",
        "  classification is graded even if the voice returns a different boolean.",
        "  A missing/invalid classification counts as wrong, never as a correct refusal.",
        "- All reported voice timing includes the classifier call. Its first token is",
        "  not a spirit token. JSON fragments are buffered until validation; an invalid",
        "  voice gets one retry, then an authored fallback. Typewriter time is excluded.",
        "- Thinking is omitted for non-thinking Gemma 3 and disabled for Qwen where",
        "  supported, using the engine's model capabilities rather than guessing.",
        "- One run per model on the normal development desktop, not an idle-machine",
        "  guarantee. No Windows/Mint run or whole-game memory measurement yet.",
        "",
        "The official catalogs list [Gemma 3 1B](https://ollama.com/library/gemma3:1b)",
        "at 806 MB under Gemma terms and [Qwen 3.5 0.8B](https://ollama.com/library/qwen3.5:0.8b)",
        "at roughly 1.2–1.3 GB under Apache 2.0. Download size does not establish RAM use.",
        "The [thinking documentation](https://docs.ollama.com/capabilities/thinking)",
        "describes capability detection and disabling supported thinking.",
        "",
        "| Model | Installed digest | Thinking control |",
        "| --- | --- | --- |",
    ]
    for model in results["models"]:
        text.append(
            f"| {model['model']} | `{model['installed']['digest']}` | "
            f"{model['run_config']['think']} |"
        )
    text += [
        "",
        "## Timing, classification and memory",
        "",
        "Warm times are seconds, **p50 / p95**; the first case is cold and excluded.",
        "Percentiles use floor((n-1)*p), without interpolation. Targets remain raw",
        "TTFT <2 s, full reply <6 s, engine <=3 GB, accuracy >=85%, all contradictions",
        "caught before display. Cold delays, maxima and the safe display boundary are",
        "reported too; no average is substituted for a failed target.",
        "",
        "| Model | Voice raw TTFT | Raw full reply | Validated display | Accuracy | Fallbacks |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in results["models"]:
        s = model["summary"]
        text.append(
            f"| {model['model']} | {pair(s['warm_raw_ttft_s'])} | "
            f"{pair(s['warm_raw_full_s'])} | {pair(s['warm_pipeline_s'])} | "
            f"{100 * s['accuracy']:.1f}% | {s['fallbacks']}/{s['cases']} |"
        )
    text += [
        "",
        "| Model | Cold raw TTFT / full / safe | Warm maximum TTFT / full / safe |",
        "| --- | ---: | ---: |",
    ]
    for model in results["models"]:
        s = model["summary"]
        cold = s["cold"]
        text.append(
            f"| {model['model']} | {seconds(cold['raw_first_token_s'])} / "
            f"{seconds(cold['raw_full_reply_s'])} / {seconds(cold['pipeline_s'])} | "
            f"{seconds(s['warm_raw_ttft_s']['max'])} / "
            f"{seconds(s['warm_raw_full_s']['max'])} / {seconds(s['warm_pipeline_s']['max'])} |"
        )
    text += [
        "",
        "| Model | Tree RSS GB | macOS physical footprint GB | Ollama size GB |",
        "| --- | ---: | ---: | ---: |",
    ]
    for model in results["models"]:
        s = model["summary"]
        text.append(
            f"| {model['model']} | {s['peak_tree_rss_bytes'] / 1e9:.2f} | "
            f"{s['peak_tree_physical_footprint_bytes'] / 1e9:.2f} | "
            f"{s['peak_ollama_size_bytes'] / 1e9:.2f} |"
        )
    text += [
        "",
        "GB is decimal. The 100 ms sampler covers the owned engine and every child.",
        "macOS physical footprint uses proc_pid_rusage/rusage_info_v2 from Apple's",
        "installed SDK. Use the largest reported memory measure for the budget,",
        "not only /api/ps. These metrics need additional GPU accounting on other OSes.",
        "",
        "## Canon audit",
        "",
        f"Audit: {audit['reviewer']}.",
        "",
        "| Model | Reviewed / generated | Flagged canon issues | "
        "Blocked | Escaped | False rejections |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in results["models"]:
        attempts = [
            (f"{model['model']}/{row['id']}/{i}", attempt)
            for row in model["rows"]
            for i, attempt in enumerate(row["attempts"])
            if "raw" in attempt
        ]
        canon = [
            (key, a) for key, a in attempts if issues.get(key, {}).get("canon_issue")
        ]
        blocked = sum(bool(a["reasons"]) for _, a in canon)
        rejected = sum(
            bool(issues.get(key, {}).get("validator_false_positive"))
            for key, _ in attempts
        )
        text.append(
            f"| {model['model']} | {sum(key in reviewed for key, _ in attempts)}/{len(attempts)} | "
            f"{len(canon)} | {blocked} | {len(canon) - blocked} | {rejected} |"
        )
    v = results["validator"]
    text += [
        "",
        f"The expanded regression suite catches {v['caught']}/{v['contradictions']} injected",
        f"false statements, rejecting {v['false_rejections']}/{v['good_controls']} valid controls.",
        "It includes escapes and Spanish false positives from the original audit.",
        "Passing this finite suite is separate from detecting new semantic errors.",
        "The validator remains an unshipped prototype; a schema cannot certify prose.",
        "",
    ]
    for model, note in audit.get("model_voice_notes", {}).items():
        text.append(f"- **{model}:** {note}")
    for issue in audit["issues"]:
        kind = "Canon" if issue.get("canon_issue") else "Voice"
        if issue.get("validator_false_positive"):
            kind = "False rejection"
        text.append(f"- **{issue['key']} ({kind}):** {issue['note']}")
    text += [
        "",
        "## Classification breakdown",
        "",
        "| Model / subset | Correct / total |",
        "| --- | ---: |",
    ]
    for model in results["models"]:
        groups: dict[str, list[Json]] = defaultdict(list)
        for row in model["rows"]:
            for key in [row["language"], row["kind"], row["object_id"]]:
                groups[key].append(row)
        for key, rows in groups.items():
            correct = sum(row["classification_correct"] for row in rows)
            text.append(f"| {model['model']} / {key} | {correct}/{len(rows)} |")
    text += [
        "",
        "## Options requiring owner direction",
        "",
        "1. **Bound dialogue to approved lines (recommended).** Keep free player input.",
        "   Have the local model classify the connection and choose a reply ID from",
        "   bilingual, authored alternatives for the selected object and legal game",
        "   state. Code resolves the ID to content; arbitrary generated words never",
        "   reach the screen. Unknown IDs/timeouts use the authored fallback. This",
        "   preserves local semantic classification and adaptive response selection,",
        "   but replaces open-ended prose generation with authored dialogue choices.",
        "   Start with the existing unrecovered/connected/recovered/unrelated/redirect",
        "   lines; add reviewed alternatives without changing the approved biography.",
        "   State filtering must exclude locked facts before inference. Rebenchmark",
        "   both existing small models, including fresh holdout and adversarial cases,",
        "   against the original resource, latency and classification gates.",
        "2. **Keep free prose and investigate another text-only model/backend.**",
        "   Preserve the current voice design, but allow another spike to find a",
        "   stronger model that fits the budget and a validation strategy that catches",
        "   indirect substitutions and invented events. No candidate is assumed to",
        "   fit, and no additional weights are downloaded or default selected here.",
        "",
        "The first option changes how the AI voices the spirit and needs the owner's",
        "approval. Neither option relaxes the canon or offline requirements. The full",
        "game, art and next feature branch remain unstarted while step 4 is stopped.",
        "",
        "## Calibration, provenance and reproduction",
        "",
        "- A four-case combined-call pilot showed poor Qwen classification; a separate",
        "  classifier was introduced without changing corpus labels.",
        "- The first 20-case split pilot scored 45% / 75%. A clearer JSON contract,",
        "  quoted player data and generic examples on different objects improved the",
        "  next pilot to 90% / 85%. These pilot cases are part of the full corpus,",
        "  so its accuracy is a development result, not an independent holdout estimate.",
        "- calibration-small-*-pilot.json/.ndjson preserve both 20-case pilots.",
        "  The full run freezes the v2 voice prompt, v3 classifier and validator.",
        "- spike/results/mac-m2-pro-16gb-small.json/.ndjson contain the complete run.",
        "- spike/results/run-source-small-sha256.json records measured source hashes.",
        "  Original Gemma 4 sources correspond to commit 3858576 and its separate hashes.",
        "- spike/audit-small.json records reviewed attempt IDs and qualitative findings.",
        "- See [spike/README.md](../spike/README.md) for the cross-platform command.",
        "- Generate this report with uv run --project api python spike/report_small.py.",
        "  spike/report.py regenerates only the historical Gemma 4 report.",
        "",
    ]
    (ROOT / "docs/BENCHMARKS_SMALL_PROSE.md").write_text("\n".join(text).rstrip() + "\n")


if __name__ == "__main__":
    main()
