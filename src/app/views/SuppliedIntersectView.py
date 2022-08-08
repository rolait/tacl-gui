from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import *

from app.views.DialogFactory import DialogFactory
from app.views.DialogView import DialogView
from app.views.components.FileSelectionWidget import FileSelectionWidget
from app.views.components.LabelWithTooltipWidget import LabelWithTooltipWidget
from app.validatable.ResultPath import ResultPath


class SuppliedIntersectView(DialogView):

    def __init__(self, dialogFactory: DialogFactory):
        super().__init__()

        self._mainVBox = QVBoxLayout()
        self._initFormGrid(dialogFactory)
        self._initButtons()

        self._removeButton.clicked.connect(self._removeResults)
        self._resultsListView.selectionModel().selectionChanged.connect(self._enableOrDisableRemoveButton)
        self._enableOrDisableRemoveButton()

        self._runButton.setDefault(True)

        self.updateTranslations()
        self._fixLayout(self._mainVBox)

    def _initFormGrid(self, dialogFactory: DialogFactory):
        formGrid = QGridLayout()
        formGrid.setSpacing(10)

        row: int = 0
        self._resultsLabel = LabelWithTooltipWidget()

        resultListWidget = QWidget()
        resultListVBox = QVBoxLayout()
        resultListVBox.setContentsMargins(0, 0, 0, 0)
        resultListWidget.setLayout(resultListVBox)

        self._resultsListView = QListView()
        self._resultsListView.setFixedHeight(75)
        self._resultsListView.setSelectionMode(QListView.ExtendedSelection)
        self._resultsListViewModel = QStandardItemModel()
        self._resultsListView.setModel(self._resultsListViewModel)


        self._addButton = QPushButton()
        self._removeButton = QPushButton()
        buttonBox = QHBoxLayout()
        buttonBox.addWidget(self._addButton)
        buttonBox.addWidget(self._removeButton)
        buttonBox.setAlignment(Qt.AlignLeft)

        resultListVBox.addWidget(self._resultsListView)
        resultListVBox.addLayout(buttonBox)

        formGrid.addWidget(self._resultsLabel, row, 0, Qt.AlignTop)
        formGrid.addWidget(resultListWidget, row, 1, Qt.AlignTop)


        row +=1
        self._outputFileLabel = LabelWithTooltipWidget()
        self._outputPathFileSelection = FileSelectionWidget(
            self,
            lambda dir: dialogFactory.showSaveFileDialog(self, dir)
        )
        formGrid.addWidget(self._outputFileLabel, row, 0)
        formGrid.addWidget(self._outputPathFileSelection, row, 1)

        self._mainVBox.addLayout(formGrid)

    def _initButtons(self):
        self._runButton = QPushButton()
        self._cancelButton = QPushButton()

        buttonHBox = QHBoxLayout()
        buttonHBox.addWidget(self._runButton)
        buttonHBox.addWidget(self._cancelButton)
        buttonHBox.setAlignment(Qt.AlignLeft)

        self._mainVBox.addLayout(buttonHBox)

    def updateTranslations(self) -> None:
        self.setWindowTitle(self.tr("Supplied Intersect"))

        self._resultsLabel.setText(self.tr("Result Files") + ":")
        self._resultsLabel.setTooltipText(self.tr(
            "Select input results (please remember NOT to run a supplied intersect on results that have already been "
            "filtered, tidied and rationalised!)"
        ))
        self._addButton.setText(self.tr("Add"))
        self._removeButton.setText(self.tr("Remove"))
        self._outputFileLabel.setText(self.tr("Output CSV File") + ":")
        self._outputFileLabel.setTooltipText(self.tr("Specify a location and name for your results."))
        self._outputPathFileSelection.setButtonText(self.tr("Select"))

        self._runButton.setText(self.tr("Run"))
        self._cancelButton.setText(self.tr("Cancel"))

    def addResults(self, results: List[ResultPath]):
        for result in results:
            from app.views.components.ListViewResultPathItem import ListViewResultPathItem
            item = ListViewResultPathItem(result)
            self._resultsListViewModel.appendRow(item)

    def getResults(self) -> List[ResultPath]:
        results: List[ResultPath] = []

        for index in range(self._resultsListViewModel.rowCount()):
            result = self._resultsListViewModel.item(index).getResultPath()
            results.append(result)

        return results

    def _removeResults(self) -> None:
        selectedIndices = reversed(sorted(self._resultsListView.selectionModel().selectedIndexes()))

        for index in selectedIndices:
            self._resultsListViewModel.takeRow(index.row())

        self._enableOrDisableRemoveButton()

    def _enableOrDisableRemoveButton(self) -> None:
        enable = len(self._resultsListView.selectionModel().selectedIndexes()) > 0
        self._removeButton.setEnabled(enable)

    def clearInput(self) -> None:
        self._outputPathFileSelection.getPathTextField().clear()
        self._resultsListViewModel.clear()

    def getOutputPath(self) -> str:
        return self._outputPathFileSelection.getPathTextField().text()

    def getRunButton(self) -> QPushButton:
        return self._runButton

    def getCancelButton(self) -> QPushButton:
        return self._cancelButton

    def getAddButton(self) -> QPushButton:
        return self._addButton

    def getRemoveButton(self) -> QPushButton:
        return self._removeButton
