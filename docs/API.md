# Local API contract

The API binds exclusively to 127.0.0.1. Electron assigns its port and permits only
the app origin through CORS. Development origins are explicit configuration.
No authentication credentials or API keys are used. The renderer cannot choose
another inference host. No model is contacted by scaffold endpoints.

`GET /health` returns HTTP 200 and `{"status":"ok"}` when the API process is ready.
It does not promise that Ollama or a model is ready. It has no side effects and
requires no model. Response content type is `application/json`.

FastAPI generates the authoritative OpenAPI contract at `/openapi.json`. A snapshot
is committed as `api/openapi.json`; regenerate with `node scripts/export-openapi.mjs`.
Future dialogue and model management contracts are added with those features.
No Postman workspace or extra credential setup is necessary for this local
single-endpoint scaffold.
