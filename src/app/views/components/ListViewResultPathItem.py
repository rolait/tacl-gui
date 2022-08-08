
from PyQt5.QtGui import QStandardItem

from app.validatable.ResultPath import ResultPath


class ListViewResultPathItem(QStandardItem):

    def __init__(self, resultPath: ResultPath):
        super().__init__(resultPath.truncate(40))
        self._resultPath = resultPath
        self.setEditable(False)

    def getResultPath(self) -> ResultPath:
        return self._resultPath