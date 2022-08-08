from typing import Callable, Optional

from PyQt5.QtWidgets import QGridLayout, QLabel

from app.tacl.TaclDatabase import TaclDatabase
from app.utils import tr
from app.views.DialogFactory import DialogFactory
from app.views.components.FileSelectionWidget import FileSelectionWidget
from app.views.components.LabelWithTooltipWidget import LabelWithTooltipWidget


class DatabasePathComponent:

    def __init__(self, row: int, formGrid: QGridLayout, fileDialogFunction: Callable[[str], Optional[str]]):
        self._label = LabelWithTooltipWidget()
        self._fileSelection = FileSelectionWidget(self, fileDialogFunction)
        formGrid.addWidget(self._label, row, 0)
        formGrid.addWidget(self._fileSelection, row, 1)

    def updateTranslations(self, tooltip: str) -> None:
        self._label.setText(tr("Database Path") + ":")
        self._label.setTooltipText(tooltip)
        self._fileSelection.setButtonText(tr("Select"))

    def getPath(self) -> str:
        return self._fileSelection.getPathTextField().text()

    def clear(self) -> None:
        self._fileSelection.getPathTextField().clear()
