from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from app.views.DialogFactory import DialogFactory
from app.views.DialogView import DialogView
from app.views.components.FileSelectionWidget import FileSelectionWidget
from app.views.components.LabelWithTooltipWidget import LabelWithTooltipWidget


class SearchView(DialogView):

    def __init__(
        self,
        dialogFactory: DialogFactory
    ):
        super().__init__()

        formGrid = QGridLayout()
        formGrid.setSpacing(10)

        row: int = 0
        row = self._initCatalogueFileSelection(row, formGrid, dialogFactory)
        row = self._initNgramsFileSelection(row, formGrid, dialogFactory)
        self._initOutputFileSelection(row, formGrid, dialogFactory)

        buttonsHBox = self._initButtons()

        mainVBox = QVBoxLayout()
        mainVBox.addLayout(formGrid)
        mainVBox.addLayout(buttonsHBox)

        self.updateTranslations()
        self._fixLayout(mainVBox)

    def _initCatalogueFileSelection(self, row: int, formGrid: QGridLayout, dialogFactory: DialogFactory) -> int:
        row += 1
        self._catalogueFileLabel = LabelWithTooltipWidget()

        self._noneRadioButton = QRadioButton()
        self._noneRadioButton.setChecked(True)
        self._selectFileRadioButton = QRadioButton()

        radioButtonHBox = QHBoxLayout()
        radioButtonHBox.addWidget(self._noneRadioButton)
        radioButtonHBox.addWidget(self._selectFileRadioButton)
        radioButtonHBox.addStretch(1)

        self._catalogueFileSelection = FileSelectionWidget(
            self,
            lambda dir: dialogFactory.showOpenExistingFileDialog(self, dir)
        )
        self._catalogueFileSelection.setDisabled(True)

        formGrid.addWidget(self._catalogueFileLabel, row, 0)
        formGrid.addLayout(radioButtonHBox, row, 1)
        row += 1
        formGrid.addWidget(self._catalogueFileSelection, row, 1)

        self._noneRadioButton.toggled.connect(lambda: self._catalogueFileSelection.setDisabled(True))
        self._selectFileRadioButton.toggled.connect(lambda: self._catalogueFileSelection.setDisabled(False))

        return row

    def _initNgramsFileSelection(self, row: int, formGrid: QGridLayout, dialogFactory: DialogFactory) -> int:
        row += 1

        self._nGramsFileLabel = LabelWithTooltipWidget()
        self._nGramsFileSelection = FileSelectionWidget(
            self,
            lambda dir: dialogFactory.showOpenExistingFileDialog(self, dir)
        )

        formGrid.addWidget(self._nGramsFileLabel, row, 0)
        formGrid.addWidget(self._nGramsFileSelection, row, 1)

        return row

    def _initOutputFileSelection(self, row: int, formGrid: QGridLayout, dialogFactory: DialogFactory) -> int:
        row += 1

        self._outputFileLabel = LabelWithTooltipWidget()
        self._outputPathFileSelection = FileSelectionWidget(
            self,
            lambda dir: dialogFactory.showSaveFileDialog(self, dir)
        )
        formGrid.addWidget(self._outputFileLabel, row, 0)
        formGrid.addWidget(self._outputPathFileSelection, row, 1)

        return row

    def _initButtons(self) -> QHBoxLayout:
        self._runTestButton = QPushButton()
        self._cancelButton = QPushButton()

        buttonsHBox = QHBoxLayout()
        buttonsHBox.addWidget(self._runTestButton)
        buttonsHBox.addWidget(self._cancelButton)
        buttonsHBox.setAlignment(Qt.AlignLeft)

        self._runTestButton.setDefault(True)

        return buttonsHBox

    def updateTranslations(self) -> None:
        self.setWindowTitle(self.tr("Search"))

        self._catalogueFileLabel.setText(self.tr("Catalogue") + ":")
        self._catalogueFileLabel.setTooltipText(self.tr(
            "Select a catalogue file. If none specified, search defaults to the whole corpus."
        ))
        self._noneRadioButton.setText(self.tr("None"))
        self._selectFileRadioButton.setText(self.tr("Select File"))
        self._catalogueFileSelection.setButtonText(self.tr("Select"))

        self._nGramsFileLabel.setText(self.tr("n-grams File") + ":")
        self._nGramsFileLabel.setTooltipText(self.tr(
            "Select a text file giving n-grams (one n-gram per line)."
        ))
        self._nGramsFileSelection.setButtonText(self.tr("Select"))

        self._outputFileLabel.setText(self.tr("Output CSV File") + ":")
        self._outputFileLabel.setTooltipText(self.tr("Specify a location and name for your results."))
        self._outputPathFileSelection.setButtonText(self.tr("Select"))

        self._runTestButton.setText(self.tr("Run Test"))
        self._cancelButton.setText(self.tr("Cancel"))

    def clearInput(self) -> None:
        self._catalogueFileSelection.getPathTextField().clear()
        self._outputPathFileSelection.getPathTextField().clear()
        self._nGramsFileSelection.getPathTextField().clear()

    def getCancelButton(self) -> QPushButton:
        return self._cancelButton

    def getRunTestButton(self) -> QPushButton:
        return self._runTestButton

    def getCataloguePath(self) -> Optional[str]:
        if self._noneRadioButton.isChecked():
            return None
        else:
            return self._catalogueFileSelection.getPathTextField().text()

    def getNgramsFilePath(self) -> str:
        return self._nGramsFileSelection.getPathTextField().text()

    def getOutputPath(self) -> str:
        return self._outputPathFileSelection.getPathTextField().text()