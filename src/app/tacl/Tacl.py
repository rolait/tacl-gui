import os
import shutil
import sys
import time
from logging import Logger, getLogger, INFO, Handler
from multiprocessing import Queue, Process
from queue import Empty
from tempfile import NamedTemporaryFile
from typing import Callable, List, Optional

import tacl.__main__ as tacl
from PyQt5.QtCore import pyqtSignal

from app.LoggerHandlerFactory import LoggerHandlerFactory
from app.tacl.TaclDiffIntersectArgs import TaclDiffIntersectArgs
from app.tacl.TaclNgramsArgs import TaclNgramsArgs
from app.tacl.TaclResultsArgs import TaclResultsArgs
from app.tacl.TaclSearchArgs import TaclSearchArgs
from app.tacl.TaclSuppliedIntersectArgs import TaclSuppliedIntersectArgs
from app.validatable.OutputCSVPath import OutputCSVPath


class Tacl:  # pragma: no cover
    """
    Manages the thread where TACL is actually called.
    """

    _TACL_LOGGER_NAME: str = "tacl.data_store"

    def __init__(self, loggerHandlerFactory: LoggerHandlerFactory):
        self._loggerHandlerFactory = loggerHandlerFactory

        self._cancelled = False

    def ngrams(self, args: TaclNgramsArgs, progressSignal: pyqtSignal(str)) -> bool:
        """
        Corresponds to
            tacl ngrams [args]
        """
        return self._runThread(progressSignal, "tacl.data_store", None, tacl.generate_ngrams, [args, None])

    def diff(self, outputPath: OutputCSVPath, args: TaclDiffIntersectArgs, progressSignal: pyqtSignal(str)) -> bool:
        """
        Corresponds to
            tacl diff [args] > [outputPath]
        """
        return self._runThread(
            progressSignal,
            "tacl.data_store",
            outputPath,
            tacl.ngram_diff,
            [args, None]
        )

    def intersect(self, outputPath: OutputCSVPath, args: TaclDiffIntersectArgs, progressSignal: pyqtSignal(str)) -> bool:
        """
        Corresponds to
            tacl intersect [args] > [outputPath]
        """

        return self._runThread(
            progressSignal,
            "tacl.data_store",
            outputPath,
            tacl.ngram_intersection,
            [args, None]
        )

    def search(
        self,
        outputPath: OutputCSVPath,
        args: TaclSearchArgs,
        resultArgs: TaclResultsArgs,
        progressSignal: pyqtSignal(str)
    ) -> bool:
        """
        Corresponds to
            tacl search [args] > [outputPath]
        followed by
            tacl results [args] > [outputPath]
        in case resultsArgs were given.
        """

        # search
        cancelled =  self._runThread(
            progressSignal,
            "tacl.data_store",
            outputPath,
            tacl.search_texts,
            [args, None]
        )

        if cancelled:
            return cancelled

        # process results
        if resultArgs is not None:
            # copy the current result file to a temporary file.
            # Delete=false because of "Permission denied" bug in some Windows environments. Will be unlinked later.
            tmpResultFile = NamedTemporaryFile(mode="w+", delete=False, encoding='utf-8')
            shutil.copy2(str(outputPath), tmpResultFile.name)
            tmpResultFile.flush()
            resultArgs.results = tmpResultFile.name

            # call tacl results.
            cancelled = self.results(outputPath, resultArgs, progressSignal)

            tmpResultFile.close()
            os.unlink(tmpResultFile.name)

        return cancelled

    def sintersect(self, outputPath: OutputCSVPath, args: TaclSuppliedIntersectArgs, progressSignal: pyqtSignal(str)) -> bool:
        """
        Corresponds to
            tacl sintersect [args] > [outputPath]
        """

        return self._runThread(
            progressSignal,
            "tacl.data_store",
            outputPath,
            tacl.supplied_intersect,
            [args, None]
        )

    def results(self, outputPath: OutputCSVPath, args: TaclResultsArgs, progressSignal: pyqtSignal(str)) -> bool:
        """
        Corresponds to
            tacl results [args] > [outputPath]
        """

        return self._runThread(
            progressSignal,
            "tacl.results",
            outputPath,
            tacl.results,
            [args, None]
        )

    def cancel(self):
        self._cancelled = True

    def _runThread(
        self,
        progressSignal: pyqtSignal(str),
        loggerName: str,
        outputPath: Optional[OutputCSVPath],
        taclCallable: Callable,
        taclCallableArgs: List
    ) -> bool:
        """
        Note:
        taclCallable can not be passed as lambda but must be passed as callable with separate arguments because
        lambdas can not be "pickled" (seems to be Windows specific problem; works on Linux). The same is true for the
        "target" argument of multiprocessing.Process.
        """
        self._cancelled = False

        # Start the tacl process
        queue: Queue = Queue()
        errorQueue: Queue = Queue()

        thread = Process(
            target=self._callTacl,
            args=(queue, errorQueue, loggerName, outputPath, taclCallable, taclCallableArgs)
        )
        thread.start()

        while thread.is_alive():
            # Pass progress information on.
            try:
                progressSignal.emit(queue.get_nowait())
            except Empty:
                pass

            # If cancelled, terminate the thread and leave the loop.
            if self._cancelled:
                thread.terminate()
                thread.join()
                break

            time.sleep(0.1)

            # re-raise potential exceptions.
            try:
                e: Exception = errorQueue.get_nowait()
                raise e
            except Empty:
                pass

        return self._cancelled

    def _callTacl(
        self,
        queue: Queue,
        errorQueue: Queue,
        loggerName: str,
        outputPath: Optional[OutputCSVPath],
        taclCallable: Callable,
        taclCallableArgs: List
    ):
        # configure the tacl logger.
        handler: Handler = self._loggerHandlerFactory.getTaclGuiHandler(queue)
        taclLogger: Logger = getLogger(loggerName)
        taclLogger.setLevel(INFO)
        taclLogger.addHandler(handler)

        # tacl prints the result to stdout. Thus, redirect stdout to the output path.
        # Note: stdout must be set within the thread which actually calls tacl, or else it will not work on Windows.
        stdout = sys.stdout

        if outputPath is not None:
            sys.stdout = open(file=str(outputPath), mode='w', encoding='utf-8')

        # call tacl.
        try:
            taclCallable(*taclCallableArgs)
        except Exception as e:
            errorQueue.put(e)

        # reset stdout.
        sys.stdout = stdout
