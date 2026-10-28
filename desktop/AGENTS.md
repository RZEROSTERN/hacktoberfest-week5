# Desktop rules

- Keep contextIsolation/sandbox on; nodeIntegration/webviewTag off. Disable packaged devTools.
- Preload exposes only the local API base. Never expose filesystem, shell or raw IPC access.
- Serve local assets through the app:// protocol with CSP hashes and path containment.
  Deny external requests, navigation, new windows and unnecessary permissions.
- Only bundled Ollama: isolated home/models, scrubbed environment, loopback dynamic ports,
  OLLAMA_NO_CLOUD=1, one loaded model and one request. Never use a system engine as fallback.
- Run engines below normal priority. A failed priority change must not prevent play.
- Stop entire process trees on quit, startup failure and cancellation. Recover recorded
  orphans only after checking identity. Unload the active model when the game closes.
- Keep platform-specific paths and process behavior in layout.ts/processes.ts/env.ts.
- Development launches use .dev/desktop-data; never share installed-app data while testing.
- Bundled binaries live in extraResources, never asar. No model weights in installers.
- From desktop/: `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`.
