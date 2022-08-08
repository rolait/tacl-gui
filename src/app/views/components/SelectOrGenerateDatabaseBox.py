from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

from app.utils import tr


class SelectOrGenerateDatabaseBox(QWidget):

    def __init__(self):
        super().__init__()

        self._label = QLabel()
        self._label.setAlignment(Qt.AlignCenter)

        self._generateButton = QPushButton()
        self._importButton = QPushButton()
        self._selectButton = QPushButton()
        self._buttonBox = QHBoxLayout()
        self._buttonBox.addStretch(1)
        self._buttonBox.addWidget(self._generateButton)
        self._buttonBox.addWidget(self._importButton)
        self._buttonBox.addWidget(self._selectButton)
        self._buttonBox.addStretch(1)
        self._buttonBox.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self._label)
        vbox.addLayout(self._buttonBox)
        vbox.setContentsMargins(20, 60, 20, 60)
        self.setLayout(vbox)

    def updateTranslations(self) -> None:
        self._label.setText(tr(
            "Please select an existing n-grams database,\n import an existing one or generate a new one."
        ))
        self._generateButton.setText(tr("Generate"))
        self._importButton.setText(tr("Import"))
        self._selectButton.setText(tr("Select"))

    def getGenerateButton(self) -> QPushButton:
        return self._generateButton

    def getImportButton(self) -> QPushButton:
        return self._importButton

    def getSelectButton(self) -> QPushButton:
        return self._selectButton