import time

from app.Database import Database
from app.Runnable import Runnable
from app.WitnessReport import WitnessReport
from app.tacl.TaclDatabase import TaclDatabase


class CheckDatabaseRunnable(Runnable):  # pragma: no cover
    _report = None

    def __init__(self, database: Database):
        super(CheckDatabaseRunnable, self).__init__(lambda progressCallback, errorCallback: self._run(database))

        self._cancelled = False
        self.getSignals().getCancelledSignal().connect(self.cancel)

    def _run(self, database: Database) -> bool:
        taclDatabase = TaclDatabase(database.getPath())
        self._report = taclDatabase.createWitnessReport(database.getCorpusPath())

        return False

    def cancel(self) -> None:
        self._cancelled = True

    def getReport(self) -> WitnessReport:
        return self._report

    def isCancelled(self) -> bool:
        return self._cancelled

