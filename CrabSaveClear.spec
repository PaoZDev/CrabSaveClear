# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['CRAB_SAVE_CLEAR.py'],
    pathex=[],
    binaries=[],
    datas=[('app.ico', 'CrabSaveClear'), ('assets\\button_1.png', 'CrabSaveClear'), ('assets\\button_2.png', 'CrabSaveClear'), ('assets\\button_3.png', 'CrabSaveClear'), ('assets\\entry_1.png', 'CrabSaveClear'), ('assets\\entry_2.png', 'CrabSaveClear'), ('assets\\entry_3.png', 'CrabSaveClear'), ('assets\\image_1.png', 'CrabSaveClear'), ('assets\\image_2.png', 'CrabSaveClear'), ('assets\\image_3.png', 'CrabSaveClear'), ('assets\\image_4.png', 'CrabSaveClear'), ('assets\\image_5.png', 'CrabSaveClear'), ('assets\\image_6.png', 'CrabSaveClear'), ('assets\\image_7.png', 'CrabSaveClear'), ('assets\\image_8.png', 'CrabSaveClear')],
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
    name='CrabSaveClear',
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
    icon=['app.ico'],
)
