import os
import platform
import shutil
import sys
import tempfile

import PyInstaller.__main__

# create dirs
VERSION = "1.0.0"
basePath = os.path.dirname(os.path.abspath(__file__))


def copyFile(name: str):
    shutil.copyfile(
        os.path.join(basePath, name),
        os.path.join(distPath, name)
    )


def replaceDir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

    os.makedirs(path)


distPath = os.path.join(basePath, "dist")
downloadPath = os.path.join(basePath, "download", VERSION)

replaceDir(distPath)
replaceDir(downloadPath)

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
    '--osx-entitlements-file', 'resources/entitlements.plist',
    '--osx-bundle-identifier', 'com.tacl-gui',
    os.path.join('src', 'main.py'),
]

if sys.platform == 'win32':
    args = [arg.replace(':', ';'
                        ) for arg in args]

PyInstaller.__main__.run(args)

# copy files
copyFile("LICENSE")
copyFile("Readme.md")

# create zip
zipFileBaseName = "TACL-GUI." + platform.system()
zipFileName = zipFileBaseName + ".zip"
tmpDir = tempfile.mkdtemp()

shutil.make_archive(os.path.join(tmpDir, zipFileBaseName), 'zip', distPath)

shutil.copyfile(
    os.path.join(tmpDir, zipFileName),
    os.path.join(downloadPath, zipFileName)
)

shutil.rmtree(tmpDir)

# create symlink
currentSymLink = os.path.join(basePath, "download", "current")
os.unlink(currentSymLink)
os.symlink(downloadPath, currentSymLink)

# Windows command: py -3.9 createExecutable.py
