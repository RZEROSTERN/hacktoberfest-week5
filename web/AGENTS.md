# Web rules

- SPA only (`ssr: false`); generated files must work over the desktop app:// origin.
- All player text comes from /content or app/locales/, in English and Spanish.
  Never put text in images; include labels, errors, settings, credits and accessibility text.
- API requests go through composables; base URL comes from window.desktop.apiBase
  or runtimeConfig.public.apiBase during development.
- Code owns the clock, memory state and endings. Save/resume must validate its input.
- The game stays playable when the model is unavailable. Make progress and latency clear.
- Use readable font sizes, accessible contrast, visible keyboard focus, reduced-motion
  support and keyboard access for every object. Inspect actual screens after UI changes.
- npm install/ci runs nuxt prepare, which ESLint and typechecking require.
- From web/: `npm run lint`, `npm run typecheck`, `npm test`, `npm run generate`.
