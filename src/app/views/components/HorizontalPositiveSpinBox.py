from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class HorizontalPositiveSpinBox(QWidget):

    def __init__(self, defaultValue: Optional[int] = None, maxValue:int = 9999):
        super().__init__()

        self._maxValue = maxValue

        self._minusButton = QPushButton("-")
        self._minusButton.setFixedWidth(25)
        self._plusButton = QPushButton("+")
        self._plusButton.setFixedWidth(25)
        self._valueField = QLineEdit()
        self._valueField.setFixedWidth(40)
        self._valueField.setAlignment(Qt.AlignCenter)

        mainHBox = QHBoxLayout()
        mainHBox.setAlignment(Qt.AlignLeft)
        mainHBox.addStretch(1)
        mainHBox.addWidget(self._minusButton)
        mainHBox.addWidget(self._valueField)
        mainHBox.addWidget(self._plusButton)
        mainHBox.setSpacing(0)
        mainHBox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(mainHBox)
        # self.setContentsMargins(0, 0, 0, 0)

        self._setValue(defaultValue)

        self._minusButton.clicked.connect(self._decreaseValue)
        self._plusButton.clicked.connect(self._increaseValue)
        self._valueField.textChanged.connect(self._checkTextValue)
        self._checkValue = True

    def _setValue(self, value: Optional[int]):
        self._checkValue = False

        if value is None or value < 1:
            self._valueField.setText("")
            self._currentValue = None
            self._valueField.setEnabled(False)
            self._minusButton.setEnabled(False)
            self._plusButton.setEnabled(True)
        elif value < self._maxValue:
            self._valueField.setText(str(value))
            self._currentValue = value
            self._valueField.setEnabled(True)
            self._minusButton.setEnabled(True)
            self._plusButton.setEnabled(True)
        else:
            self._valueField.setText(str(self._maxValue))
            self._currentValue = self._maxValue
            self._minusButton.setEnabled((True))
            self._valueField.setEnabled(True)
            self._plusButton.setEnabled(False)

        self._checkValue = True

    def _decreaseValue(self):
        if self._currentValue is None:
            self._setValue(None)
            return

        self._setValue(self._currentValue - 1)

    def _increaseValue(self):
        if self._currentValue is None:
            self._setValue(1)
        else:
            self._setValue(self._currentValue + 1)

    def _checkTextValue(self) -> None:
        if not self._checkValue:
            return

        text = self._valueField.text().strip().replace("+", "")

        if len(text) == 0:
            self._setValue(None)
        elif text.isdigit():
            intValue = int(text)

            if intValue > self._maxValue:
                self._setValue(self._maxValue)
            else:
                self._currentValue = intValue
        else:
            self._setValue(self._currentValue)

    def getValue(self) -> Optional[int]:
        return self._currentValue
