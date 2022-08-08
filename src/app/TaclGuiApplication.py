import os
import sqlite3
import sys
from sqlite3 import Connection
from typing import List

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication


from app.Container import Container
from app.utils import resource


class TaclGuiApplication(QApplication):

    def __init__(self, baseDir: str, argv: List[str]):
        super().__init__(argv)
        self._baseDir = baseDir

        icon = QIcon()
        icon.addFile(resource("app-icon-16.png"), QSize(16, 16))
        icon.addFile(resource("app-icon-24.png"), QSize(24, 24))
        icon.addFile(resource("app-icon-32.png"), QSize(32, 32))
        icon.addFile(resource("app-icon-48.png"), QSize(48, 48))
        icon.addFile(resource("app-icon-256.png"), QSize(256, 256))
        self.setWindowIcon(icon)

        self.setStyleSheet(
            """
            QLabel, QPushButton, QRadioButton, QLineEdit, QGroupBox, QSpinBox, QComboBox
            {
                font-family: Helvetica, Arial, Ubuntu, Liberation Sans, SimSun; 
                font-size: 1rem;
            }
            """
        )

    def run(self) -> None:
        connection = self._initDatabase()

        container = Container(self, connection)
        container.mainController().run()

        sys.exit(self.exec_())

    def _initDatabase(self) -> Connection:
        databasePath = os.path.join(self._baseDir, "tacl-gui.db")

        connection = sqlite3.connect(databasePath)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = 1")

        with open(resource("tacl-gui.db.structure.sql"), "r") as databaseSqlFile:
            connection.executescript(databaseSqlFile.read())

        return connection
