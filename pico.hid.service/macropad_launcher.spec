# -*- mode: python ; coding: utf-8 -*-
import subprocess


# the following full path to signtool probably must be changed if
# the signing of the executabel fails
path_to_signtool_exe = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.19041.0/x86/signtool.exe"

block_cipher = None

a = Analysis(['macropad_launcher.py'],
             pathex=['C:\\Users\\Simu\\Projects\\raspi.pico.collection\\pico.hid.service'],
             binaries=[],
             datas=[('.\\dist\\makro_icon.ico', '.')],
             hiddenimports=['win32timezone','pynput.keyboard._win32', 'pynput.mouse._win32', 'PyQt5'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='macropad_launcher',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='.\dist\makro_icon.ico' )
#coll = COLLECT(exe,
#               a.binaries,
#               a.zipfiles,
#               a.datas, 
#               strip=False,
#               upx=True,
#               upx_exclude=[],
#               name='macropad_launcher')

# Code-sign the generated executable
# subprocess.call([
#   path_to_signtool_exe,
#   "sign",
#   "/A",
#   "/T", "http://timestamp.digicert.com",
#   '.\pico.hid.service\dist\macropad_launcher.exe',
#], shell=True)