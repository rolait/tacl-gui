from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from _pytest.stash import D

from app.validatable import DatabaseNGramLengths
from app.views.DialogFactory import DialogFactory
from app.views.DialogView import DialogView
from app.views.components.CorpusPathComponent import CorpusPathComponent
from app.views.components.DatabaseNameComponent import DatabaseNameComponent
from app.views.components.DatabasePathComponent import DatabasePathComponent
from app.views.components.FileSelectionWidget import FileSelectionWidget
from app.views.components.LabelWithTooltipWidget import LabelWithTooltipWidget
from app.views.components.NGramsGroupBox import NGramsGroupBox


class GenerateDatabaseView(DialogView):

    def __init__(
        self,
        dialogFactory: DialogFactory
    ):
        super().__init__()

        self._initDatabaseGroupBox(dialogFactory)

        self._ngramsGroupBox = NGramsGroupBox()
        self._ngramsGroupBox.setMinMaxValues(2, 99, 2, 99)

        self._initButtons()

        mainVBox = QVBoxLayout()
        mainVBox.addStretch(1)
        mainVBox.addWidget(self._databaseGroupBox)
        mainVBox.addWidget(self._ngramsGroupBox)
        mainVBox.addLayout(self._buttonHBox)

        self._fixLayout(mainVBox)
        self.updateTranslations()
        self.clearInput()

    def _initDatabaseGroupBox(
        self,
        dialogFactory: DialogFactory
    ) -> None:

        formGrid = QGridLayout()
        self._databaseGroupBox = QGroupBox()
        self._databaseGroupBox.setLayout(formGrid)

        row: int = 0
        self._databaseNameComponent = DatabaseNameComponent(row, formGrid)
        row += 1
        self._databasePathComponent = DatabasePathComponent(
            row, formGrid, lambda dir: dialogFactory.showSaveFileDialog(self, dir)
        )
        row += 1
        self._corpusPathComponent = CorpusPathComponent(row, self, formGrid, dialogFactory)

    def _initButtons(self) -> None:
        self._buttonHBox = QHBoxLayout()
        self._createButton = QPushButton()
        self._cancelButton = QPushButton()

        self._buttonHBox.addWidget(self._createButton)
        self._buttonHBox.addWidget(self._cancelButton)
        self._buttonHBox.setAlignment(Qt.AlignLeft)

        self._createButton.setDefault(True)

    def updateTranslations(self) -> None:
        self.setWindowTitle(self.tr("Generate n-grams Database"))

        self._databaseGroupBox.setTitle(self.tr("Database"))

        self._databaseNameComponent.updateTranslations()
        self._databasePathComponent.updateTranslations(self.tr(
            "Select a location where the generated n-grams database should be saved (e.g. \"my-database.db\")."
        ))
        self._corpusPathComponent.updateTranslations()

        self._createButton.setText(self.tr("Generate"))
        self._cancelButton.setText(self.tr("Cancel"))

        self._ngramsGroupBox.updateTranslations()

    def clearInput(self) -> None:
        self._databaseNameComponent.clear()
        self._databasePathComponent.clear()
        self._corpusPathComponent.clear()

        self._ngramsGroupBox.setValues(2, 2)

    def getCancelButton(self) -> QPushButton:
        return self._cancelButton

    def getGenerateButton(self) -> QPushButton:
        return self._createButton

    def getDatabaseName(self) -> str:
        return self._databaseNameComponent.getName()

    def getDatabasePath(self) -> str:
        return self._databasePathComponent.getPath()

    def getCorpusPath(self) -> str:
        return self._corpusPathComponent.getPath()

    def getNGramLengths(self) -> DatabaseNGramLengths:
        return self._ngramsGroupBox.getInput()

