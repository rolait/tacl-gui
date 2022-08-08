import os
from pathlib import Path
from typing import Optional

from PyQt5.QtCore import Qt

from app.validatable.CorpusPath import CorpusPath
from app.Database import Database
from app.validatable.DatabaseNGramLengths import DatabaseNGramLengths
from app.validatable.DatabaseName import DatabaseName
from app.repositories.DatabaseRepository import DatabaseRepository
from app.views.DialogFactory import DialogFactory
from app.validatable.Id import Id
from app.validatable.NewDatabasePath import NewDatabasePath
from app.tacl.TaclRunner import TaclRunner
from app.inputValidator.InputValidatorFactory import InputValidatorFactory
from app.views.GenerateDatabaseView import GenerateDatabaseView
from app.utils import tr


class GenerateDatabaseController:
    _progressDialog = None
    _generatedDatabaseId: Optional[Id] = None

    def __init__(
        self, view: GenerateDatabaseView,
        dialogFactory: DialogFactory,
        inputValidatorFactory: InputValidatorFactory,
        databaseRepository: DatabaseRepository,
        taclRunner: TaclRunner,
    ):
        self._inputValidatorFactory = inputValidatorFactory
        self._dialogFactory = dialogFactory
        self._view = view
        self._databaseRepository = databaseRepository
        self._taclRunner = taclRunner

        self._view.getGenerateButton().clicked.connect(lambda: self._create())
        self._view.getCancelButton().clicked.connect(lambda: self._close())

    def run(self) -> Optional[Id]:  # pragma: no cover
        self._generatedDatabaseId = None
        self._view.showAsApplicationModal()

        return self._generatedDatabaseId

    def _create(self) -> None:
        inputValidator = self._inputValidatorFactory.getInputValidator()

        name: Optional[DatabaseName] = inputValidator.validate(
            lambda: DatabaseName(self._view.getDatabaseName())
        )

        if self._databaseRepository.existsByName(name):
            errorMsg = tr("A database with the name '{}' already exists.").format(str(name))
            inputValidator.addError(errorMsg)

        databasePath: Optional[NewDatabasePath] = inputValidator.validate(
            lambda: NewDatabasePath(self._view.getDatabasePath())
        )
        corpusPath: Optional[CorpusPath] = inputValidator.validate(
            lambda: CorpusPath(self._view.getCorpusPath())
        )
        ngramLengths = self._view.getNGramLengths()

        if inputValidator.showErrorDialog():
            return
        elif not self._dialogFactory.showOverwriteDialogIfFileExistent(databasePath, self._view):
            return

        # if another database exists with the same path delete it first. At this point the user was already asked
        # whether he wants to replace the database file or not.
        if Path(str(databasePath)).exists():
            os.unlink(str(databasePath))

        self._databaseRepository.deleteByDatabasePath(databasePath)

        self._taclRunner.runNgrams(
            databasePath,
            corpusPath,
            ngramLengths,
            self._view,
            tr("Generating n-grams Database"),
            lambda: self._saveDatabaseAndClose(name, databasePath, corpusPath, ngramLengths)
        )

    def _close(self):
        self._view.close()

    def _saveDatabaseAndClose(
        self,
        name: DatabaseName,
        databasePath: NewDatabasePath,
        corpusPath: CorpusPath,
        ngramLengths: DatabaseNGramLengths
    ):
        database = Database(
            None,
            name,
            databasePath.toExistingDatabasePath(),
            corpusPath,
            ngramLengths
        )

        # save the database
        self._generatedDatabaseId = self._databaseRepository.save(database)

        self._view.clearInput()
        self._close()
