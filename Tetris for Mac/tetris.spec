# -*- mode: python -*-
a = Analysis(['tetris.py'],
             pathex=['/Users/Kairavi/Documents/Carnegie Mellon University/Coursework/2.3/Fundamentals of Programming/Tetris/Tetris for Mac'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='tetris',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='tetris')
app = BUNDLE(coll,
             name='tetris.app',
             icon=None)
