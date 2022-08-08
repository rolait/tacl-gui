from logging import Handler, INFO, LogRecord
from multiprocessing import Queue

class TaclGuiLoggerHandler(Handler):  # pragma: no cover

    def __init__(self, queue: Queue):
        Handler.__init__(self)
        self._queue = queue
        self.setLevel(INFO)

    def emit(self, record: LogRecord):
        self._queue.put(self.format(record))
