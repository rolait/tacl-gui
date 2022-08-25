#!/usr/bin/python3
# -*- coding: utf-8 -*-
import multiprocessing
import os
import sys
from traceback import format_exception

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt

from app.ExceptionHandler import ExceptionHandler
from app.TaclGuiApplication import TaclGuiApplication


# Any uncaught exception will be shown in an error dialog.
def handleException(exctype, value, traceback):
    exceptionHandler = ExceptionHandler()
    stackTrace = ''.join(format_exception(exctype, value, traceback))
    exceptionHandler.handle(value, stackTrace)


sys.excepthook = handleException

if __name__ == '__main__':
    # Required for Windows.
    multiprocessing.freeze_support()

    # Determine the base path

    if sys.platform == 'darwin':
        # On macOS: Use "~/Library/Application Support/TACL" instead of the current working directory to comply with macOS Sandbox restrictions
        from AppKit import NSSearchPathForDirectoriesInDomains, NSApplicationSupportDirectory, NSUserDomainMask
        # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
        # Last parameter 'True' for expanding the tilde into a fully qualified path
        baseDir = os.path.join(NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, NSUserDomainMask, True)[0], "TACL")
        # Create the directory if it does not exist yet
        os.makedirs(baseDir, exist_ok=True)
    elif getattr(sys, 'frozen', False) and sys.executable:
        baseDir = os.path.dirname(sys.executable)
    else:
        baseDir = os.path.dirname(os.path.abspath(__file__))

    # Enable automatic DPI scaling.
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    TaclGuiApplication(baseDir, []).run()
