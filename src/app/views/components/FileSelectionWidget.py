from typing import Callable, Optional

from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QLineEdit


class FileSelectionWidget(QWidget):

    def __init__(self, parent: QWidget, fileDialogFunction: Callable[[str], Optional[str]]):
        super().__init__()
        self._fileDialogFunction = fileDialogFunction
        self._parent = parent

        self.pathTextField = QLineEdit()
        self.pathTextField.setMinimumWidth(250)
        self.pathTextField.setMaxLength(2500)
        self._openFileDialogButton = QPushButton()

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.pathTextField)
        hbox.addWidget(self._openFileDialogButton)

        self.setLayout(hbox)
        self._openFileDialogButton.clicked.connect(self._openFileDialog)

    def setButtonText(self, buttonText: str) -> None:
        self._openFileDialogButton.setText(buttonText)

    def _openFileDialog(self):
        path = self._fileDialogFunction(self.pathTextField.text())

        if path is not None:
            self.pathTextField.setText(path)

    def getPathTextField(self) -> QLineEdit:
        return self.pathTextField
