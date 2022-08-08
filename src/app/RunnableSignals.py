from PyQt5.QtCore import QObject, pyqtSignal


class RunnableSignals(QObject):  # pragma: no cover
    # Must be instantiated as class attributes and not in the constructor or else the exception
    # "'PyQt5.QtCore.pyqtSignal' object has no attribute 'emit'"
    # is thrown.
    _finishedSignal = pyqtSignal()
    _cancelledSignal = pyqtSignal()
    _errorSignal = pyqtSignal(Exception)
    _progressSignal = pyqtSignal(str)

    def getFinishedSignal(self) -> pyqtSignal():
        return self._finishedSignal

    def getCancelledSignal(self) -> pyqtSignal():
        return self._cancelledSignal

    def getErrorSignal(self) -> pyqtSignal(Exception):
        return self._errorSignal

    def getProgressSignal(self) -> pyqtSignal(str):
        return self._progressSignal
