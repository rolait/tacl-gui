from PyQt5.QtWidgets import QGridLayout, QLabel, QDialog

from app.utils import tr
from app.views.DialogFactory import DialogFactory
from app.views.components.FileSelectionWidget import FileSelectionWidget


class CorpusPathComponent:

    def __init__(self, row: int, view: QDialog, formGrid: QGridLayout, dialogFactory: DialogFactory):
        self._corpusPathLabel = QLabel()
        self._corpusPathFileSelection = FileSelectionWidget(
            self,
            lambda dir: dialogFactory.showOpenExistingDirectoryDialog(view, dir)
        )
        formGrid.addWidget(self._corpusPathLabel, row, 0)
        formGrid.addWidget(self._corpusPathFileSelection, row, 1)

    def updateTranslations(self) -> None:
        self._corpusPathLabel.setText(tr("Corpus Path") + ":")
        self._corpusPathFileSelection.setButtonText(tr("Select"))

    def getPath(self) -> str:
        return self._corpusPathFileSelection.getPathTextField().text()

    def clear(self) -> None:
        self._corpusPathFileSelection.getPathTextField().clear()