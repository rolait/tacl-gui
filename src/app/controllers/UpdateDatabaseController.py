from typing import Optional

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
from app.utils import tr
from app.views.UpdateDatabaseView import UpdateDatabaseView


class UpdateDatabaseController:
    _currentDatabase: Database = None

    def __init__(
        self,
        view: UpdateDatabaseView,
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

        self._view.getUpdateButton().clicked.connect(lambda: self._update())
        self._view.getCancelButton().clicked.connect(lambda: self._close())

    def run(self, database: Database) -> None:
        self._currentDatabase = database

        self._view.setDatabase(database)
        self._view.showAsApplicationModal()

    def _update(self) -> None:
        inputValidator = self._inputValidatorFactory.getInputValidator()

        name: Optional[DatabaseName] = inputValidator.validate(
            lambda: DatabaseName(self._view.getDatabaseName())
        )

        if str(self._currentDatabase.getName()) != str(name) and self._databaseRepository.existsByName(name):
            errorMsg = tr("Can not rename database. A database with the name '{}' already exists.")\
                .format(str(name))
            inputValidator.addError(errorMsg)

        ngramLengths = self._view.getNGramLengths()

        if inputValidator.showErrorDialog():
            return

        self._taclRunner.runNgrams(
            self._currentDatabase.getPath(),
            self._currentDatabase.getCorpusPath(),
            ngramLengths,
            self._view,
            tr("Updating n-grams Database"),
            lambda: self._saveDatabaseAndClose(name, ngramLengths)
        )

    def _close(self):
        self._view.close()

    def _saveDatabaseAndClose(
        self,
        name: DatabaseName,
        ngramLengths: DatabaseNGramLengths
    ):
        self._currentDatabase.setName(name)
        self._currentDatabase.setNgramLengths(ngramLengths)
        self._generatedDatabaseId = self._databaseRepository.save(self._currentDatabase)

        self._view.close()
