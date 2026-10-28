# Workflow rules

- Production is master only; integration is develop. Never target another production branch.
- Pin third-party actions to full commit SHAs with version comments. Read action.yml
  at the pinned revision before changing inputs. Validate YAML with actionlint.
- contents: read by default. Only the draft-release job gets contents: write.
- Releases stay drafts; never publish automatically. Verify version and master ancestry.
- Release PRs into master build macOS arm64 DMG, Windows x64 NSIS, Linux x64 AppImage/deb.
- Call repository scripts so local npm run dist and the build matrix cannot diverge.
- Verify downloaded binaries with pinned checksums. Stop above the 1.5 GB installer limit.
- No cloud inference or model weights on CI. Integration tests stay excluded.
- No configured API keys/secrets. Release authentication uses only GitHub's job token.
- Full installer builds can be requested on develop PRs with ci-build; dispatch needs
  workflows on master. Inspect failed job logs before pushing a fix.
