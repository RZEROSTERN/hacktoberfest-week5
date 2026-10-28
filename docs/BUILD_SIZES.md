# Installer build evidence

Sizes are the actual installer files, before model download. The limit is
1.5 GB per installer. SHA-256 identifies the specific build; later rebuilds
may differ. Smoke tests start the bundled Ollama and API, check the model
catalog and authored fallback, and verify representative web assets. They do
not replace installation or a human playtest.

| Build | Environment | Size | SHA-256 |
| --- | --- | ---: | --- |
| macOS arm64 DMG, 0.1.0 | M2 Pro local build, 2026-10-27 | 288.5 MB | `82faea2b9cde29043fe30aa82a708c651767834a42bc05babc38c3692dc6f787` |
| macOS arm64 DMG, 0.1.0 | macOS CI | 290.2 MB | `5dc8a827bd012066f9d109d5d0e6428048329028fce63f539c19496c6a793676` |
| Windows x64 NSIS, 0.1.0 | Windows Server 2022 CI | 169.1 MB | `107a475c06151bdb435ab13c4b76c34935de69fb56d2e0634872ba3922dfda81` |
| Linux x64 AppImage, 0.1.0 | Ubuntu 22.04 CI | 196.4 MB | `0cb19708837f7b3d84e8671e8b8d929e0040f146febf721f4ed6d4e2af22d2bb` |
| Linux x64 deb, 0.1.0 | Ubuntu 22.04 CI | 158.5 MB | `b3182493d907f5c0d8b0f0a529e005cfc0ee94abb3a43800da64398699a6ffff` |

All three CI jobs passed their pre-package and packaged smoke checks in [run
40631491354](https://github.com/RZEROSTERN/hacktoberfest-week5/actions/runs/40631491354).
The macOS build is ad-hoc signed and not notarized. Installation on the owner’s
machines, a fresh model download and an independent playtest remain outstanding.
