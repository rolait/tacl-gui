import os
import sys

from PyQt5.QtWidgets import QApplication


def tr(text: str) -> str:
    return QApplication.translate("tacl-gui", text)


def resource(path: str) -> str:
    try:
        # noinspection PyUnresolvedReferences,PyProtectedMember
        # sys._MEIPASS will be set by pyinstaller in case the application is bundled in an executable file.
        basePath = os.path.join(sys._MEIPASS, "resources")
    except AttributeError:
        basePath = os.path.abspath("../resources")

    return os.path.join(basePath, path)
