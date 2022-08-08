from typing import List, Optional

from PyQt5.QtWidgets import QMessageBox, QWidget

from app.Database import Database
from app.views.DialogFactory import DialogFactory
from app.controllers.DifferenceIntersectController import DifferenceIntersectController
from app.controllers.FilterRationaliseController import FilterRationaliseController
from app.validatable.OutputCSVPath import OutputCSVPath
from app.validatable.ResultPath import ResultPath
from app.repositories.ResultRepository import ResultRepository
from app.ResultType import ResultType
from app.views.SuppliedIntersectView import SuppliedIntersectView
from app.tacl.TaclRunner import TaclRunner
from app.inputValidator.InputValidatorFactory import InputValidatorFactory
from app.utils import tr


class SuppliedIntersectController:
    _database: Database = None

    _DEFAULT_LABEL = "SuppliedResults{}"

    def __init__(
        self,
        view: SuppliedIntersectView,
        taclRunner: TaclRunner,
        resultRepository: ResultRepository,
        dialogFactory: DialogFactory,
        differenceIntersectController: DifferenceIntersectController,
        filterRationaliseController: FilterRationaliseController,
        inputValidatorFactory: InputValidatorFactory
    ):
        self._resultRepository = resultRepository
        self._taclRunner = taclRunner
        self._view = view
        self._dialogFactory = dialogFactory
        self._differenceIntersectController = differenceIntersectController
        self._filterRationaliseController = filterRationaliseController
        self._inputValidatorFactory = inputValidatorFactory

        self._view.getRunButton().clicked.connect(self._run)
        self._view.getAddButton().clicked.connect(self._add)
        self._view.getCancelButton().clicked.connect(self._close)

    def run(self, database: Database, parentView: QWidget) -> None:
        self._database = database

        results = self._resultRepository.findTwoMostRecentForSuppliedIntersect(self._database)
        resultsCount = len(results)

        if resultsCount < 2 and self._cancelTest(resultsCount, parentView):
            return

        if len(self._view.getResults()) < 2:
            self._view.clearInput()
            self._view.addResults(results)

        self._view.showAsApplicationModal()

    def _cancelTest(self, resultsCount: int, parentView: QWidget) -> bool:
        self._view.clearInput()

        if resultsCount == 0:
            message = self._view.tr(
                "Supplied intersect requires two sets of results to work from, but you have not generated any "
                "results for this database yet. Please conduct at least two difference or intersect tests "
                "before you attempt a supplied intersect."
            )
        else:
            message = self._view.tr(
                "Supplied intersect requires two sets of results to work from, but you have only "
                "generated one set for this database. Please conduct another difference or intersect test "
                "before you attempt a supplied intersect."
            )

        cancelled = self._dialogFactory.showConfirmationDialog(
            self._view.tr("Info"),
            message,
            parentView,
            self._view.tr("OK"), self._view.tr("Select Results Manually"),
            QMessageBox.Ok
        )

        if cancelled:
            self._differenceIntersectController.run(self._database)
            return True

        return False

    def _close(self):
        self._view.close()

    def _add(self) -> None:
        resultStrings = self._dialogFactory.showOpenExistingFilesDialog(self._view, "")

        inputValidator = self._inputValidatorFactory.getInputValidator()
        results: List[ResultPath] = []
        alreadyAddedResults = {str(r): None for r in self._view.getResults()}

        for resultString in resultStrings:
            result: Optional[ResultPath] = inputValidator.validate(lambda: ResultPath(resultString))

            if result is None:
                continue

            if str(result) in alreadyAddedResults:
                continue

            results.append(result)

        inputValidator.showErrorDialog()

        self._view.addResults(results)

    def _run(self) -> None:
        inputValidator = self._inputValidatorFactory.getInputValidator()

        results = self._view.getResults()
        if len(results) < 2:
            inputValidator.addError(
                self._view.tr("At least two result files must be selected for a supplied intersect"))

        outputPath: Optional[OutputCSVPath] = inputValidator.validate(lambda: OutputCSVPath(self._view.getOutputPath()))

        if inputValidator.showErrorDialog():
            return
        elif not self._dialogFactory.showOverwriteDialogIfFileExistent(outputPath, self._view):
            return

        self._runCommand(results, outputPath)

    def _runCommand(self, results: List[ResultPath], outputPath: OutputCSVPath):
        # set default labels
        labels: List[str] = []

        for i in range(1, len(results) + 1):
            labels.append(self._DEFAULT_LABEL.format(i))

        self._taclRunner.runSuppliedIntersect(
            self._database, results, labels, outputPath, self._view, lambda: self._saveResultAndClose(outputPath)
        )

    def _saveResultAndClose(self, outputPath: OutputCSVPath):
        resultPath = outputPath.toResultPath()
        self._resultRepository.save(self._database, resultPath, ResultType.SUPPLIED_INTERSECT)
        self._view.clearInput()
        self._close()
