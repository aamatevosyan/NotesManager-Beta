# -*- mode: python ; coding: utf-8 -*-

from glob import glob

block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=['jsonpickle','simplejson'],
             hookspath=['notes'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

datas = []
datas += glob('/notes/*')
datas += glob('/resources/*')

a.datas = datas

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Notes Manager',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True , icon='C:\\Users\\newap\\Desktop\\NotesManager-Beta\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='NotesManager')
