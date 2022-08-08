from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from app.Database import Database
from app.validatable import DatabaseNGramLengths
from app.views.DialogView import DialogView
from app.views.components.DatabaseNameComponent import DatabaseNameComponent
from app.views.components.NGramsGroupBox import NGramsGroupBox


class UpdateDatabaseView(DialogView):

    def __init__(
        self
    ):
        super().__init__()

        formGrid = QGridLayout()

        row: int = 0
        self._databaseNameComponent = DatabaseNameComponent(row, formGrid)

        self._ngramsGroupBox = NGramsGroupBox()
        self._initButtons()

        mainVBox = QVBoxLayout()
        mainVBox.addStretch(1)
        mainVBox.addLayout(formGrid)
        mainVBox.addWidget(self._ngramsGroupBox)
        mainVBox.addLayout(self._buttonHBox)

        self._fixLayout(mainVBox)
        self.updateTranslations()

    def _initButtons(self) -> None:
        self._buttonHBox = QHBoxLayout()
        self._updateButton = QPushButton()
        self._cancelButton = QPushButton()

        self._buttonHBox.addWidget(self._updateButton)
        self._buttonHBox.addWidget(self._cancelButton)
        self._buttonHBox.setAlignment(Qt.AlignLeft)

        self._updateButton.setDefault(True)

    def updateTranslations(self) -> None:
        self.setWindowTitle(self.tr("Update n-grams Database"))

        self._databaseNameComponent.updateTranslations()

        self._updateButton.setText(self.tr("Update"))
        self._cancelButton.setText(self.tr("Cancel"))

        self._ngramsGroupBox.updateTranslations()

    def setDatabase(self, database: Database) -> None:
        self._databaseNameComponent.setName(str(database.getName()))

        self._ngramsGroupBox.setMinMaxValues(
            2, database.getNGramMinLength(),
            database.getNGramMaxLength(), 99
        )
        self._ngramsGroupBox.setValues(database.getNGramMinLength(), database.getNGramMaxLength())

    def getCancelButton(self) -> QPushButton:
        return self._cancelButton

    def getUpdateButton(self) -> QPushButton:
        return self._updateButton

    def getDatabaseName(self) -> str:
        return self._databaseNameComponent.getName()

    def getNGramLengths(self) -> DatabaseNGramLengths:
        return self._ngramsGroupBox.getInput()

