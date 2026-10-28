# Installer build evidence

Sizes are the actual installer files, before model download. The limit is
1.5 GB per installer. SHA-256 identifies the specific build; later rebuilds
may differ. Smoke tests start the bundled Ollama and API, check the model
catalog and authored fallback, and verify representative web assets. They do
not replace installation or a human playtest.

| Build | Environment | Size | SHA-256 |
| --- | --- | ---: | --- |
| macOS arm64 DMG, 0.1.0 | M2 Pro local build, 2026-10-27 | 288.5 MB | `82faea2b9cde29043fe30aa82a708c651767834a42bc05babc38c3692dc6f787` |
| Windows x64 NSIS | CI matrix | Pending | Pending |
| Linux x64 AppImage | CI matrix | Pending | Pending |
| Linux x64 deb | CI matrix | Pending | Pending |

The macOS build's pre-package and packaged smoke checks passed. It is ad-hoc
signed and not notarized. Windows and Linux CI results, installation on the
owner's machines, a fresh model download and an independent playtest remain
outstanding.
