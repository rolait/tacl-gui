import sqlite3
from typing import Optional

from app.DatabaseLoadingException import DatabaseLoadingException
from app.inputValidator.InputValidator import InputValidator
from app.inputValidator.ValidationError import ValidationError
from app.tacl.TaclDatabase import TaclDatabase
from app.validatable.CorpusPath import CorpusPath
from app.Database import Database
from app.validatable.DatabaseNGramLengths import DatabaseNGramLengths
from app.validatable.DatabaseName import DatabaseName
from app.repositories.DatabaseRepository import DatabaseRepository
from app.validatable.DatabasePath import DatabasePath
from app.views.DialogFactory import DialogFactory
from app.validatable.Id import Id
from app.validatable.NewDatabasePath import NewDatabasePath
from app.tacl.TaclRunner import TaclRunner
from app.inputValidator.InputValidatorFactory import InputValidatorFactory
from app.utils import tr
from app.views.ImportDatabaseView import ImportDatabaseView
from app.views.UpdateDatabaseView import UpdateDatabaseView


class ImportDatabaseController:
    _importedDatabaseId: Optional[Id] = None

    def __init__(
        self,
        view: ImportDatabaseView,
        dialogFactory: DialogFactory,
        inputValidatorFactory: InputValidatorFactory,
        databaseRepository: DatabaseRepository
    ):
        self._inputValidatorFactory = inputValidatorFactory
        self._dialogFactory = dialogFactory
        self._view = view
        self._databaseRepository = databaseRepository

        self._view.getImportButton().clicked.connect(lambda: self._import())
        self._view.getCancelButton().clicked.connect(lambda: self._close())

    def run(self) -> Optional[Id]:
        self._importedDatabaseId = None
        self._view.showAsApplicationModal()

        return self._importedDatabaseId

    def _import(self) -> None:
        inputValidator = self._inputValidatorFactory.getInputValidator()

        name = self._databaseRepository.validateName(self._view.getDatabaseName(), inputValidator, True)

        databasePath: Optional[NewDatabasePath] = inputValidator.validate(
            lambda: DatabasePath(self._view.getDatabasePath())
        )
        corpusPath: Optional[CorpusPath] = inputValidator.validate(
            lambda: CorpusPath(self._view.getCorpusPath())
        )

        # check whether a database with the name or database path already exists.
        existingDatabaseName = self._databaseRepository.findNameByDatabasePath(databasePath)
        if existingDatabaseName is not None:
            inputValidator.addError(tr(
                "The selected database file is already associated with the database '{}'.".format(existingDatabaseName)
            ))

        # get the ngram lengths
        if databasePath is not None and corpusPath is not None:
            taclDatabase = TaclDatabase(databasePath)

            try:
                nGramLengths = taclDatabase.extractNgramLengths()

            except ValidationError as error:
                inputValidator.addError(
                    tr("The selected database is invalid or maybe not a database file: {}").format(str(error))
                )

        if inputValidator.showErrorDialog():
            return

        database = Database(None, name, databasePath, corpusPath, nGramLengths)
        self._importedDatabaseId = self._databaseRepository.save(database)

        self._view.clearInput()
        self._close()

    def _close(self):
        self._view.close()
