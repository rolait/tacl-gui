from typing import Optional

from app.Database import Database
from app.views.DialogFactory import DialogFactory
from app.views.FilterRationaliseView import FilterRationaliseView
from app.validatable.OutputCSVPath import OutputCSVPath
from app.validatable.ResultPath import ResultPath
from app.repositories.ResultRepository import ResultRepository
from app.tacl.TaclRunner import TaclRunner
from app.inputValidator.InputValidatorFactory import InputValidatorFactory


class FilterRationaliseController:
    _database: Database = None

    def __init__(
        self,
        view: FilterRationaliseView,
        inputValidatorFactory: InputValidatorFactory,
        resultRepository: ResultRepository,
        taclRunner: TaclRunner,
        dialogFactory: DialogFactory
    ):
        self._view = view
        self._databaseRepository = resultRepository
        self._inputValidatorFactory = inputValidatorFactory
        self._taclRunner = taclRunner
        self._dialogFactory = dialogFactory

        # actions
        self._view.getRunFiltersButton().clicked.connect(lambda: self._runFilters())
        self._view.getCancelButton().clicked.connect(lambda: self._close())

    def run(self, database: Database, resultPath: ResultPath = None) -> None:
        self._database = database

        if resultPath is not None:
            self._view.setResultPath(resultPath)

        self._view.showAsApplicationModal()

    def _close(self) -> None:
        self._view.close()

    def _runFilters(self) -> None:
        inputValidator = self._inputValidatorFactory.getInputValidator()

        resultPath: Optional[ResultPath] = \
            inputValidator.validate(lambda: ResultPath(self._view.getResultFile()))
        outputPath: Optional[OutputCSVPath] = \
            inputValidator.validate(lambda: OutputCSVPath(self._view.getOutputPath()))

        if inputValidator.showErrorDialog():
            return
        elif not self._dialogFactory.showOverwriteDialogIfFileExistent(outputPath, self._view):
            return

        self._taclRunner.runFilterRationalise(
            self._database, resultPath,
            self._view.getMinCount(), self._view.getMaxCount(),
            self._view.getMinSize(), self._view.getMaxSize(),
            self._view.getMinCountWorks(), self._view.getMaxCountWorks(),
            self._view.getMinWorks(), self._view.getMaxWorks(),
            outputPath,
            self._view, self._saveAndClose
        )

    def _saveAndClose(self):
        self._view.clearInput()
        self._close()
