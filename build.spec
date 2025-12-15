# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Inntinnsic
Usage: pyinstaller build.spec
"""
import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Collect NudeNet model files
nudenet_datas = collect_data_files('nudenet', include_py_files=False)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=nudenet_datas + [
        # NudeNet model files are collected above
    ],
    hiddenimports=[
        'nudenet',
        'nudenet.nudenet',
        'PIL',
        'PIL._tkinter_finder',
        'tkinter',
        'ttkthemes',
        'customtkinter',
        'sklearn',
        'sklearn.ensemble',
        'sklearn.tree',
        'onnxruntime',
        'onnxruntime.capi',
        'onnxruntime.capi._pybind_state',
    ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Inntinnsic',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to False to hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Application icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Inntinnsic',
)
