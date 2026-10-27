from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ["entrypoint.py"],
    pathex=["."],
    datas=[("prompts", "prompts"), ("../content", "content")],
    hiddenimports=collect_submodules("uvicorn"),
    excludes=["tkinter", "pytest", "mypy", "ruff"],
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name="last-candle-api", console=True, upx=False)
