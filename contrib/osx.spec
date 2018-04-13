# -*- mode: python -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

import sys
for i, x in enumerate(sys.argv):
    if x == '--name':
        VERSION = sys.argv[i+1]
        break
else:
    raise BaseException('no version')

home = '../'
block_cipher=None

# see https://github.com/pyinstaller/pyinstaller/issues/2005
hiddenimports = ['_scrypt']

datas = [
    (home+'lib/currencies.json', 'electrum'),
    (home+'lib/servers.json', 'electrum'),
    (home+'lib/wordlist/english.txt', 'electrum/wordlist'),
    (home+'lib/locale', 'electrum/locale'),
    (home+'plugins', 'electrum_plugins'),
]

# Workaround for "Retro Look":
binaries = [b for b in collect_dynamic_libs('PyQt5') if 'macstyle' in b[0]]

# Add libusb so Trezor will work
binaries += [(home + "dist/libusb-1.0.dylib", ".")]

# We don't put these files in to actually include them in the script but to make the Analysis method scan them for imports
a = Analysis([home+'electrum',
              home+'gui/qt/main_window.py',
              home+'gui/text.py',
              home+'lib/util.py',
              home+'lib/wallet.py',
              home+'lib/simple_config.py',
              home+'lib/bitcoin.py',
              home+'lib/dnssec.py',
              home+'lib/commands.py',
              home+'plugins/cosigner_pool/qt.py',
              home+'plugins/email_requests/qt.py',
              home+'plugins/trezor/client.py',
              home+'plugins/trezor/qt.py',
              home+'plugins/keepkey/qt.py',
              home+'plugins/ledger/qt.py',
              ],
             binaries=binaries,
             datas=datas,
             hiddenimports=hiddenimports,
             hookspath=[])

# http://stackoverflow.com/questions/19055089/pyinstaller-onefile-warning-pyconfig-h-when-importing-scipy-or-scipy-signal
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,
          name='Electrum-FTC',
          debug=False,
          strip=False,
          upx=True,
          icon=home+'electrum/electrum.icns',
          console=False)

app = BUNDLE(exe,
             version = VERSION,
             name='Electrum-FTC.app',
             icon=home+'electrum/electrum.icns',
             bundle_identifier=None,
             info_plist = {
                 'NSHighResolutionCapable':'True'
             }
)
