from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit

from app.utils import tr
from app.views.components.LabelWithTooltipWidget import LabelWithTooltipWidget


class DatabaseNameComponent:

    def __init__(self,  row: int, formGrid: QGridLayout):
        self._label = LabelWithTooltipWidget()
        self._textField = QLineEdit()
        self._textField.setMaxLength(50)
        self._textField.setMinimumWidth(250)
        formGrid.addWidget(self._label, row, 0)
        formGrid.addWidget(self._textField, row, 1)

    def updateTranslations(self) -> None:
        self._label.setText(tr("Name") + ":")
        self._label.setTooltipText(tr("Give your database a name (e.g. \"My Database\")."))

    def getName(self) -> str:
        return self._textField.text()

    def clear(self) -> None:
        self._textField.clear()

    def setName(self, name: str) -> None:
        self._textField.setText(name)