# Local model spike

- Run real inference only on the maintainer's computer, never CI/cloud.
- Use a dedicated bundled Ollama process, isolated home/models, dynamic loopback port,
  one loaded model and one request. Never unload or stop someone else's engine.
- Model tags are benchmark inputs, not runtime defaults. Compare both required models.
- The fixed corpus has 20 bilingual cases per object, including relevant, irrelevant
  and adversarial messages. Do not tune expected labels to model answers.
- Record cold/warm timing, raw token latency versus validated display latency, model
  digest, engine/options, RSS for the entire owned process tree, and Ollama allocation.
- Results contain only synthetic fixtures. Never benchmark real player conversations.
- Rules/schema validation is not proof of semantic correctness. Audit raw outputs,
  record missed contradictions and false positives, and state sample-size limits.
- No model may be selected if any required target fails; stop before the spike PR.
- Unload the model and stop the full owned process tree on success, failure or interrupt.
