from typing import Callable
from PyQt5.QtCore import QRunnable, pyqtSignal, pyqtSlot

from app.RunnableSignals import RunnableSignals


class Runnable(QRunnable):  # pragma: no cover

    def __init__(self, function: Callable[[pyqtSignal(str), pyqtSignal(Exception)], bool]):
        super().__init__()
        self._function = function
        self.signals = RunnableSignals()

    @pyqtSlot()
    def run(self):
        try:
            cancelled = self._function(self.signals.getProgressSignal(), self.signals.getErrorSignal())

            if cancelled:
                self.signals.getCancelledSignal().emit()
            else:
                self.signals.getFinishedSignal().emit()

        except Exception as exception:
            self.signals.getErrorSignal().emit(exception)

    def getSignals(self) -> RunnableSignals:
        return self.signals
