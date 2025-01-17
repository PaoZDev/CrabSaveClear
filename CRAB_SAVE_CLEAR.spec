# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['CRAB_SAVE_CLEAR.py'],
    pathex=[],
    binaries=[],
    datas=[('assets\\button_1.png', '.'), ('assets\\button_2.png', '.'), ('assets\\button_3.png', '.'), ('assets\\entry_1.png', '.'), ('assets\\entry_2.png', '.'), ('assets\\entry_3.png', '.'), ('assets\\image_1.png', '.'), ('assets\\image_2.png', '.'), ('assets\\image_3.png', '.'), ('assets\\image_4.png', '.'), ('assets\\image_5.png', '.'), ('assets\\image_6.png', '.'), ('assets\\image_7.png', '.'), ('assets\\image_8.png', '.')],
    hiddenimports=[],
    hookspath=[],
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
    name='CRAB_SAVE_CLEAR',
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
)
