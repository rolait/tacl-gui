from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLayout


class DialogView(QDialog):

    def _fixLayout(self, layout: QLayout):
        self.setLayout(layout)
        self.setMaximumWidth(self.width())
        layout.setSizeConstraint(QLayout.SetFixedSize)

    def showAsApplicationModal(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()
