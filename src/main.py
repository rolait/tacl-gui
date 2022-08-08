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
    if getattr(sys, 'frozen', False) and sys.executable:
        baseDir = os.path.dirname(sys.executable)
    else:
        baseDir = os.path.dirname(os.path.abspath(__file__))

    # Enable automatic DPI scaling.
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    TaclGuiApplication(baseDir, []).run()
