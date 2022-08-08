from typing import Callable, Optional

from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QLineEdit, QCheckBox, QLabel

from app.utils import tr


class CheckboxWithTextFieldWidget(QWidget):

    def __init__(self, labelText: str):
        super().__init__()

        self._labelText = labelText;
        self._textField = QLineEdit()
        self._label = QLabel()

        self._checkBox = QCheckBox()

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self._checkBox)
        hbox.addWidget(self._label)
        hbox.addWidget(self._textField)

        self.setLayout(hbox)

        self.updateTranslations()
        self.setDisabled(True)

        self._checkBox.clicked.connect(lambda: self.setDisabled(not self._checkBox.isChecked()))

    def updateTranslations(self):
        self._label.setText(tr(self._labelText) + ":")

    def getValue(self) -> Optional[str]:
        if self._checkBox.isChecked():
            return self._textField.text()
        else:
            return None

    def clear(self) -> None:
        self._checkBox.setChecked(False)
        self._textField.clear()
        self.setDisabled(True)

    def setDisabled(self, disabled: bool) -> None:
        self._textField.setDisabled(disabled)
        self._label.setDisabled(disabled)
