from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from app.views.DialogFactory import DialogFactory
from app.views.DialogView import DialogView
from app.views.components.CorpusPathComponent import CorpusPathComponent
from app.views.components.DatabaseNameComponent import DatabaseNameComponent
from app.views.components.DatabasePathComponent import DatabasePathComponent


class ImportDatabaseView(DialogView):

    def __init__(
        self,
        dialogFactory: DialogFactory
    ):
        super().__init__()

        formGrid = QGridLayout()

        row: int = 0
        self._nameLabel = QLabel()
        self._nameTextField = QLineEdit()
        self._nameTextField.setMaxLength(50)
        formGrid.addWidget(self._nameLabel, row, 0)
        formGrid.addWidget(self._nameTextField, row, 1)

        row: int = 0
        self._databaseNameComponent = DatabaseNameComponent(row, formGrid)
        row += 1
        self._databasePathComponent = DatabasePathComponent(
            row, formGrid, lambda dir: dialogFactory.showOpenExistingFileDialog(self, dir)
        )
        row += 1
        self._corpusPathComponent = CorpusPathComponent(row, self, formGrid, dialogFactory)

        self._initButtons()

        mainVBox = QVBoxLayout()
        mainVBox.addStretch(1)
        mainVBox.addLayout(formGrid)
        mainVBox.addLayout(self._buttonHBox)

        self._fixLayout(mainVBox)
        self.updateTranslations()

    def _initButtons(self) -> None:
        self._buttonHBox = QHBoxLayout()
        self._importButton = QPushButton()
        self._cancelButton = QPushButton()

        self._buttonHBox.addWidget(self._importButton)
        self._buttonHBox.addWidget(self._cancelButton)
        self._buttonHBox.setAlignment(Qt.AlignLeft)

        self._importButton.setDefault(True)

    def updateTranslations(self) -> None:
        self.setWindowTitle(self.tr("Import existing n-grams Database"))

        self._nameLabel.setText(self.tr("Name") + ":")

        self._databaseNameComponent.updateTranslations()
        self._databasePathComponent.updateTranslations(self.tr(
            "Select the location of an existing database."
        ))
        self._corpusPathComponent.updateTranslations()

        self._importButton.setText(self.tr("Import"))
        self._cancelButton.setText(self.tr("Cancel"))

    def clearInput(self) -> None:
        self._databaseNameComponent.clear()
        self._databasePathComponent.clear()
        self._corpusPathComponent.clear()

    def getCancelButton(self) -> QPushButton:
        return self._cancelButton

    def getImportButton(self) -> QPushButton:
        return self._importButton

    def getDatabaseName(self) -> str:
        return self._databaseNameComponent.getName()

    def getDatabasePath(self) -> str:
        return self._databasePathComponent.getPath()

    def getCorpusPath(self) -> str:
        return self._corpusPathComponent.getPath()
