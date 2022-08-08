from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

from app.utils import tr


class NoDatabaseBox(QWidget):

    def __init__(self):
        super().__init__()

        self._label = QLabel()
        self._label.setAlignment(Qt.AlignCenter)

        self._generateButton = QPushButton()
        self._importButton = QPushButton()
        self._buttonBox = QHBoxLayout()
        self._buttonBox.addStretch(1)
        self._buttonBox.addWidget(self._generateButton)
        self._buttonBox.addWidget(self._importButton)
        self._buttonBox.addStretch(1)
        self._buttonBox.setAlignment(Qt.AlignCenter)


        vbox = QVBoxLayout()
        vbox.addWidget(self._label)
        vbox.addLayout(self._buttonBox)
        vbox.setContentsMargins(20, 60, 20, 60)
        self.setLayout(vbox)

    def updateTranslations(self) -> None:
        self._label.setText(tr(
            "Click on \"Generate\" to create a new n-grams\n"
            "database or on \"Import\" to import an existing one."
        ))
        self._generateButton.setText(tr("Generate"))
        self._importButton.setText(tr("Import"))

    def getGenerateButton(self) -> QPushButton:
        return self._generateButton

    def getImportButton(self) -> QPushButton:
        return self._importButton