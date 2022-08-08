from typing import Optional

from app.validatable.AsymmetricLabel import AsymmetricLabel
from app.validatable.CataloguePath import CataloguePath
from app.Database import Database
from app.views.DialogFactory import DialogFactory
from app.views.DifferenceIntersectView import DifferenceIntersectView
from app.validatable.OutputCSVPath import OutputCSVPath
from app.repositories.ResultRepository import ResultRepository
from app.ResultType import ResultType
from app.tacl.TaclRunner import TaclRunner
from app.inputValidator.InputValidatorFactory import InputValidatorFactory


class DifferenceIntersectController:
    _database: Optional[Database] = None

    def __init__(
        self,
        view: DifferenceIntersectView,
        taclRunner: TaclRunner,
        inputValidatorFactory: InputValidatorFactory,
        resultRepository: ResultRepository,
        dialogFactory: DialogFactory
    ):
        self._view = view
        self._taclRunner = taclRunner
        self._inputValidatorFactory = inputValidatorFactory
        self._resultRepository = resultRepository
        self._dialogFactory = dialogFactory

        self._view.getRunTestButton().clicked.connect(lambda: self._runTest())
        self._view.getCancelButton().clicked.connect(lambda: self._close())

    def run(self, database: Database) -> None:
        self._database = database
        self._view.showAsApplicationModal()

    def _close(self) -> None:
        self._view.close()

    def _runTest(self) -> None:
        inputValidator = self._inputValidatorFactory.getInputValidator()

        cataloguePath: Optional[CataloguePath] = \
            inputValidator.validate(lambda: CataloguePath(self._view.getCataloguePath()))
        outputPath: Optional[OutputCSVPath] = \
            inputValidator.validate(lambda: OutputCSVPath(self._view.getOutputPath()))

        asymmetricLabel: Optional[AsymmetricLabel] = self._view.getAsymmetricLabel()
        if self._view.isDifferenceChecked() and asymmetricLabel is not None:
            asymmetricLabel = inputValidator.validate(lambda: AsymmetricLabel(asymmetricLabel))

        if inputValidator.showErrorDialog():
            return
        elif not self._dialogFactory.showOverwriteDialogIfFileExistent(outputPath, self._view):
            return

        if self._view.isDifferenceChecked():
            self._taclRunner.runDiff(
                self._database,
                cataloguePath, outputPath, asymmetricLabel,
                self._view,
                lambda: self._processFinishedResult(outputPath, ResultType.DIFFERENCE)
            )
        else:
            self._taclRunner.runIntersect(
                self._database,
                cataloguePath, outputPath,
                self._view,
                lambda: self._processFinishedResult(outputPath, ResultType.INTERSECT)
            )

    def _processFinishedResult(self, outputPath: OutputCSVPath, type: ResultType):
        self._resultPath = outputPath.toResultPath()
        self._resultRepository.save(self._database, self._resultPath, type)

        self._view.clearInput()
        self._close()