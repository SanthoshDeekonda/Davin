# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Davin.py'],
    pathex=[],
    binaries=[],
    datas=[('.venv/Lib/site-packages/plotly/package_data', 'plotly/package_data'), ('.venv/Lib/site-packages/kaleido-0.1.0.post1.dist-info', 'kaleido-0.1.0.post1.dist-info')],
    hiddenimports=[],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Davin',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assests\\mainWindow\\logo\\Davin_Logo_ico.ico'],
)
