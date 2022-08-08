from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from app.views.DialogView import DialogView


class SelectDatabaseView(DialogView):

    def __init__(self):
        super().__init__()

        self._selectDatabaseLabel = QLabel()

        self._databaseComboBox = QComboBox()
        self._databaseComboBox.setFixedWidth(350)

        self._selectButton = QPushButton()
        self._cancelButton = QPushButton()

        buttonHBox = QHBoxLayout()
        buttonHBox.addWidget(self._selectButton)
        buttonHBox.addWidget(self._cancelButton)
        buttonHBox.setAlignment(Qt.AlignLeft)

        mainVBox = QVBoxLayout()
        mainVBox.addWidget(self._selectDatabaseLabel)
        mainVBox.addWidget(self._databaseComboBox)
        mainVBox.addLayout(buttonHBox)

        self.updateTranslations()
        self._fixLayout(mainVBox)

    def updateTranslations(self) -> None:
        self.setWindowTitle(self.tr("Database Selection"))

        self._selectDatabaseLabel.setText(self.tr("Select Database") + ":")
        self._selectButton.setText(self.tr("Select"))
        self._cancelButton.setText(self.tr("Cancel"))

    def getSelectButton(self) -> QPushButton:
        return self._selectButton

    def getCancelButton(self) -> QPushButton:
        return self._cancelButton

    def getDatabaseComboBox(self) -> QComboBox:
        return self._databaseComboBox
