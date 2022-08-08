from multiprocessing import Queue

from app.tacl.TaclGuiLoggerHandler import TaclGuiLoggerHandler


class LoggerHandlerFactory:  # pragma: no cover

    def getTaclGuiHandler(self, queue: Queue) -> TaclGuiLoggerHandler:
        return TaclGuiLoggerHandler(queue)
