from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from app.utils import resource


class LabelWithTooltipWidget(QWidget):

    def __init__(self):
        super().__init__()

        self._label = QLabel()

        self._icon = QLabel()
        self._icon.setPixmap(QPixmap(resource("tooltip-icon.png")))

        hbox = QHBoxLayout()
        hbox.addWidget(self._label)
        hbox.addWidget(self._icon)
        hbox.addStretch(1)
        hbox.setSpacing(3)
        hbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(hbox)

    def setText(self, text: str) -> None:
        self._label.setText(text)

    def setTooltipText(self, text: str) -> None:
        tooltipText = "<qt>{}</qt>".format(text)
        self._icon.setToolTip(tooltipText)

    # def mousePressEvent(self, event):
    #     self._icon.toolTip().showText()