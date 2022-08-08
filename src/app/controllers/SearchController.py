import os
from tempfile import NamedTemporaryFile
from typing import Optional

from app.validatable.CataloguePath import CataloguePath
from app.Database import Database
from app.validatable.NgramsFilePath import NgramsFilePath
from app.validatable.OutputCSVPath import OutputCSVPath
from app.views.DialogFactory import DialogFactory
from app.views.SearchView import SearchView
from app.tacl.TaclRunner import TaclRunner
from app.inputValidator.InputValidatorFactory import InputValidatorFactory


class SearchController:
    _database: Optional[Database] = None
    _catalogueFile: Optional[NamedTemporaryFile] = None

    def __init__(
        self,
        view: SearchView,
        inputValidatorFactory: InputValidatorFactory,
        taclRunner: TaclRunner,
        dialogFactory: DialogFactory
    ):
        self._view = view
        self._taclRunner = taclRunner
        self._inputValidatorFactory = inputValidatorFactory
        self._dialogFactory = dialogFactory

        # actions
        self._view.getRunTestButton().clicked.connect(lambda: self._runTest())
        self._view.getCancelButton().clicked.connect(lambda: self._close())

    def run(self, database: Database) -> None:
        self._database = database
        self._view.showAsApplicationModal()

    def _close(self) -> None:
        self._closeCatalogueFile()
        self._view.close()

    def _runTest(self) -> None:
        # check input
        inputValidator = self._inputValidatorFactory.getInputValidator()

        if self._view.getCataloguePath() is None:
            self._closeCatalogueFile()
            self._catalogueFile = self._database.getCorpusPath().createBaseCatalogueFile()

            cataloguePath = CataloguePath(self._catalogueFile.name)
        else:
            cataloguePath = \
                inputValidator.validate(lambda: CataloguePath(self._view.getCataloguePath()))

        ngramsFilePath: Optional[NgramsFilePath] = \
            inputValidator.validate(lambda: NgramsFilePath(self._view.getNgramsFilePath()))
        outputPath: Optional[OutputCSVPath] = \
            inputValidator.validate(lambda: OutputCSVPath(self._view.getOutputPath()))

        if inputValidator.showErrorDialog():
            return
        elif not self._dialogFactory.showOverwriteDialogIfFileExistent(outputPath, self._view):
            return

        self._taclRunner.runSearch(
            self._database,
            cataloguePath,
            ngramsFilePath,
            outputPath,
            True,   # always group by witness
            self._view,
            lambda: self._clearInputAndClose()
        )

    def _clearInputAndClose(self):
        self._view.clearInput()
        self._close()

    def _closeCatalogueFile(self):
        if self._catalogueFile is not None:
            self._catalogueFile.close()
            os.unlink(self._catalogueFile.name)
            self._catalogueFile = None
