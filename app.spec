# -*- mode: python ; coding: utf-8 -*-

import os
block_cipher = None

import sys
sys.setrecursionlimit(10000)


a = Analysis(
    ['app.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[],
    hiddenimports=['torchxrayvision'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

for b in a.binaries.copy():  # Traver the binaries.
    for d in a.datas:  #  Traverse the datas.
        if b[1].endswith(d[0]):  # If duplicate found.
            a.binaries.remove(b)  # Remove the duplicate.
            break

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='app',
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
