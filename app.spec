# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all Streamlit data files
streamlit_data = collect_data_files('streamlit')

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py', '.'),
        ('.env', '.'),
    ] + streamlit_data,
    hiddenimports=[
        'streamlit',
        'streamlit.web',
        'streamlit.runtime',
        'streamlit.runtime.scriptrunner',
        'streamlit.runtime.app_session',
        'streamlit.runtime.caching',
        'streamlit.runtime.metrics_util',
        'streamlit.runtime.secrets',
        'streamlit.elements',
        'streamlit.elements.balloons',
        'streamlit.elements.json',
        'streamlit.elements.layouts',
        'streamlit.elements.markdown',
        'streamlit.elements.media',
        'streamlit.elements.utils',
        'streamlit.components',
    ] + collect_submodules('streamlit'),
    hookspath=[],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='InterviewApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
