import os
import platform
import shutil
import sys
import tempfile

import PyInstaller.__main__

basePath = os.path.dirname(os.path.abspath(__file__))
distPath = os.path.join(basePath, "dist")

# remove dist path
if os.path.exists(distPath):
    shutil.rmtree(distPath)

os.mkdir(distPath)

# create executable
args = [
    '--onefile',
    '--windowed',
    '--name', 'TACL-GUI',
    '--icon', 'resources/app-icon.ico',
    '--add-data', 'resources/tooltip-icon.png:resources',
    '--add-data', 'resources/app-icon-16.png:resources',
    '--add-data', 'resources/app-icon-24.png:resources',
    '--add-data', 'resources/app-icon-32.png:resources',
    '--add-data', 'resources/app-icon-48.png:resources',
    '--add-data', 'resources/app-icon-256.png:resources',
    '--add-data', 'resources/tacl-gui.db.structure.sql:resources',
    os.path.join('src', 'main.py'),
]

if sys.platform == 'win32':
    args = [arg.replace(':', ';'
                        ) for arg in args]

PyInstaller.__main__.run(args)

# copy licenses
shutil.copyfile(
    os.path.join(basePath, "LICENSE"),
    os.path.join(distPath, "LICENSE")
)

# create zip
zipFileBaseName = "TACL-GUI." + platform.system()
zipFileName = zipFileBaseName + ".zip"
tmpDir = tempfile.mkdtemp()

shutil.make_archive(os.path.join(tmpDir, zipFileBaseName), 'zip', distPath)

shutil.copyfile(
    os.path.join(tmpDir, zipFileName),
    os.path.join(distPath, zipFileName)
)

shutil.rmtree(tmpDir)

# Windows command: py -3.9 createExecutable.py