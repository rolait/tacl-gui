from collections import Callable
from typing import Optional, List

import tacl
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QProgressDialog, QWidget

from app.validatable.AsymmetricLabel import AsymmetricLabel
from app.validatable.CataloguePath import CataloguePath
from app.validatable.CorpusPath import CorpusPath
from app.Database import Database
from app.validatable.DatabaseNGramLengths import DatabaseNGramLengths
from app.validatable.FilePath import FilePath
from app.views.DialogFactory import DialogFactory
from app.validatable.NewDatabasePath import NewDatabasePath
from app.validatable.NgramsFilePath import NgramsFilePath
from app.validatable.OutputCSVPath import OutputCSVPath
from app.validatable.ResultPath import ResultPath
from app.Runnable import Runnable
from app.tacl.Tacl import Tacl
from app.tacl.TaclDiffIntersectArgs import TaclDiffIntersectArgs
from app.tacl.TaclNgramsArgs import TaclNgramsArgs
from app.tacl.TaclResultsArgs import TaclResultsArgs
from app.tacl.TaclSearchArgs import TaclSearchArgs
from app.tacl.TaclSuppliedIntersectArgs import TaclSuppliedIntersectArgs
from app.utils import tr

DEFAULT_TOKENIZER = "cbeta"

class TaclRunner:  # pragma: no cover

    def __init__(
        self,
        tacl: Tacl,
        dialogFactory: DialogFactory,
        qThreadPool: QThreadPool
    ):
        self._tacl = tacl
        self._dialogFactory = dialogFactory
        self._qThreadPool = qThreadPool

    def runNgrams(
        self,
        databasePath: FilePath,
        corpusPath: CorpusPath,
        ngramLengths: DatabaseNGramLengths,
        parentView: QWidget,
        progressDialogTitle: str,
        finishedCallable: Callable
    ):
        args = TaclNgramsArgs(
            str(corpusPath),
            str(databasePath),
            ngramLengths.getMinLength(),
            ngramLengths.getMaxLength()
        )

        self._run(
            parentView,
            progressDialogTitle,
            finishedCallable,
            lambda progressCallback, errorCallback: self._tacl.ngrams(args, progressCallback)
        )

    def runIntersect(
        self,
        database: Database,
        cataloguePath: CataloguePath,
        outputPath: OutputCSVPath,
        parentView: QWidget,
        finishedCallable: Callable
    ):
        args = args = TaclDiffIntersectArgs(
            str(cataloguePath),
            str(database.getCorpusPath()),
            str(database.getPath()),
        )

        self._run(
            parentView,
            str("Running Intersect"),
            finishedCallable,
            lambda progressCallback, errorCallback: self._tacl.intersect(outputPath, args, progressCallback)
        )

    def runDiff(
        self,
        database: Database,
        cataloguePath: CataloguePath,
        outputPath: OutputCSVPath,
        asymmetricLabel: Optional[AsymmetricLabel],
        parentView: QWidget,
        finishedCallable: Callable
    ):
        asymmetricLabelStr = str(asymmetricLabel) if asymmetricLabel is not None else None

        args = args = TaclDiffIntersectArgs(
            str(cataloguePath),
            str(database.getCorpusPath()),
            str(database.getPath()),
            asymmetricLabelStr
        )

        self._run(
            parentView,
            tr("Running difference"),
            finishedCallable,
            lambda progressCallback, errorCallback: self._tacl.diff(outputPath, args, progressCallback)
        )

    def runSearch(
        self,
        database: Database,
        cataloguePath: CataloguePath,
        ngramsFilePath: NgramsFilePath,
        outputCSVPath: OutputCSVPath,
        groupByWitness: bool,
        parentView: QWidget,
        finishedCallable: Callable
    ):
        args = TaclSearchArgs(
            str(cataloguePath),
            str(database.getCorpusPath()),
            str(database.getPath()),
            [str(ngramsFilePath)]
        )

        resultArgs: Optional[TaclResultsArgs] = None
        if groupByWitness:
            resultArgs = TaclResultsArgs(
                results=str(outputCSVPath),
                tokenizer=DEFAULT_TOKENIZER,
                group_by_witness=True
            )

        self._run(
            parentView,
            tr("Running Search"),
            finishedCallable,
            lambda progressCallback, errorCallback: self._tacl.search(outputCSVPath, args, resultArgs, progressCallback)
        )

    def runSuppliedIntersect(
        self,
        database: Database,
        results: List[ResultPath],
        labels: List[str],
        outputPath: OutputCSVPath,
        parentView: QWidget,
        finishedCallable: Callable
    ):
        resultList = list(map(lambda result: str(result), results))
        args = TaclSuppliedIntersectArgs(str(database.getPath()), labels, resultList)

        self._run(
            parentView, tr("Running Supplied Intersect"), finishedCallable,
            lambda progressCallback, errorCallback: self._tacl.sintersect(outputPath, args, progressCallback)
        )

    def runFilterRationalise(
        self,
        database: Database,
        resultPath: ResultPath,
        minCount: Optional[int], maxCount: Optional[int],
        minSize: Optional[int], maxSize: Optional[int],
        minCountWorks: Optional[int], maxCountWorks: Optional[int],
        minWorks: Optional[int], maxWorks: Optional[int],
        outputPath: OutputCSVPath,
        parentView: QWidget,
        finishedCallable: Callable
    ):
        corpusPath = str(database.getCorpusPath())

        # noinspection PyProtectedMember
        if tacl.Results._is_intersect_results(resultPath.toDataFrame()):
            extend = corpusPath
            reduce = True
        else:
            extend = None
            reduce = False

        args = TaclResultsArgs(
            results=str(resultPath),
            tokenizer=DEFAULT_TOKENIZER,
            min_count=minCount, max_count=maxCount,
            min_size=minSize, max_size=maxSize,
            min_count_work=minCountWorks, max_count_work=maxCountWorks,
            min_works=minWorks, max_works=maxWorks,
            extend=extend,
            reduce=reduce,

            # hardwired defaults
            zero_fill=corpusPath,
            collapse_witnesses=True,
            add_label_count=True
        )

        self._run(
            parentView, tr("Running Filter/Rationalise"), finishedCallable,
            lambda progressCallback, errorCallback: self._tacl.results(outputPath, args, progressCallback)
        )

    def _run(
        self,
        parentView: QWidget,
        progressDialogTitle: str,
        finishedCallable: Callable,
        taclCallable: Callable,
    ):
        runnable: Runnable = Runnable(taclCallable)

        progressDialog = self._dialogFactory.showProgressDialog(
            parentView,
            progressDialogTitle,
            0,  # indeterminate
            tr("Initialising") + "...",
            runnable
        )
        progressDialog.canceled.connect(self._tacl.cancel)

        signals = runnable.getSignals()
        signals.getErrorSignal().connect(lambda exception: self._handleErrorSignal(progressDialog, exception))
        signals.getCancelledSignal().connect(lambda: self._tacl.cancel())
        signals.getFinishedSignal().connect(lambda: self._handleFinishedSignal(progressDialog, finishedCallable))

        self._qThreadPool.start(runnable)

    def _handleCancelSignal(self) -> None:
        pass

    def _handleErrorSignal(self, progressDialog: QProgressDialog, exception: Exception) -> None:
        self._dialogFactory.showTaclError(exception)
        progressDialog.close()

    def _handleFinishedSignal(self, progressDialog: QProgressDialog, finshedCallable: Callable) -> None:
        progressDialog.setLabelText(progressDialog.tr("Finished") + ".")
        progressDialog.close()

        finshedCallable()
