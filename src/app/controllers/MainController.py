import os
import textwrap
import time
from logging import Logger
from typing import Optional

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMessageBox, QProgressDialog

from app.CheckDatabaseRunnable import CheckDatabaseRunnable
from app.Database import Database
from app.DatabaseLoadingException import DatabaseLoadingException
from app.Runnable import Runnable
from app.controllers.DifferenceIntersectController import DifferenceIntersectController
from app.controllers.FilterRationaliseController import FilterRationaliseController
from app.controllers.GenerateDatabaseController import GenerateDatabaseController
from app.controllers.ImportDatabaseController import ImportDatabaseController
from app.controllers.SearchController import SearchController
from app.controllers.SelectDatabaseController import SelectDatabaseController
from app.controllers.SuppliedIntersectController import SuppliedIntersectController
from app.controllers.UpdateDatabaseController import UpdateDatabaseController
from app.repositories.DatabaseRepository import DatabaseRepository
from app.repositories.SettingsRepository import SettingsRepository
from app.tacl.TaclDatabase import TaclDatabase
from app.tacl.TaclRunner import TaclRunner
from app.utils import tr
from app.validatable.Id import Id
from app.views.DialogFactory import DialogFactory
from app.views.MainView import MainView


class MainController:
    _runnable = None
    _currentDatabase: Optional[Database] = None

    def __init__(
            self,
            view: MainView,
            databaseRepository: DatabaseRepository,
            generateDatabaseController: GenerateDatabaseController,
            importDatabaseController: ImportDatabaseController,
            updateDatabaseController: UpdateDatabaseController,
            differenceIntersectController: DifferenceIntersectController,
            searchController: SearchController,
            logger: Logger,
            settingsRepository: SettingsRepository,
            dialogFactory: DialogFactory,
            selectDatabaseController: SelectDatabaseController,
            suppliedIntersectController: SuppliedIntersectController,
            filterRationaliseController: FilterRationaliseController,
            taclRunner: TaclRunner,
            qThreadPool: QThreadPool
    ):
        self._view = view
        self._databaseRepository = databaseRepository
        self._generateDatabaseController = generateDatabaseController
        self._importDatabaseController = importDatabaseController
        self._updateDatabaseController = updateDatabaseController
        self._logger = logger
        self._settingsRepository = settingsRepository
        self._differenceIntersectController = differenceIntersectController
        self._searchController = searchController
        self._dialogFactory = dialogFactory
        self._selectDatabaseController = selectDatabaseController
        self._suppliedIntersectController = suppliedIntersectController
        self._filterRationaliseController = filterRationaliseController
        self._taclRunner = taclRunner
        self._qThreadPool = qThreadPool

        self._settings = settingsRepository.find()

        # actions
        self._view.getNoDatabaseBox().getGenerateButton().clicked.connect(lambda: self._generate())
        self._view.getNoDatabaseBox().getImportButton().clicked.connect(lambda: self._import())
        self._view.getSelectOrGenerateDatabaseBox().getGenerateButton().clicked.connect(lambda: self._generate())
        self._view.getSelectOrGenerateDatabaseBox().getImportButton().clicked.connect(lambda: self._import())
        self._view.getSelectOrGenerateDatabaseBox().getSelectButton().clicked.connect(lambda: self._select())
        self._view.getDifferenceIntersectButton().clicked.connect(lambda: self._differenceIntersect())
        self._view.getSearchButton().clicked.connect(lambda: self._search())
        self._view.getSuppliedIntersectButton().clicked.connect(lambda: self._suppliedIntersect())
        self._view.getFilterRationaliseButton().clicked.connect(lambda: self._filterRationalise())
        self._view.getDatabaseInfoBox().getUpdateButton().clicked.connect(lambda: self._update())
        self._view.getDatabaseInfoBox().getDeleteButton().clicked.connect(lambda: self._delete())

        self._view.getMenuBar().getGenerateAction().triggered.connect(lambda: self._generate())
        self._view.getMenuBar().getImportAction().triggered.connect(lambda: self._import())
        self._view.getMenuBar().getSelectAction().triggered.connect(lambda: self._select())
        self._view.getMenuBar().getExitAction().triggered.connect(lambda: self._exit())

    def run(self) -> None:
        self._view.center()
        self._view.show()

        self._setCurrentDatabase(self._settings.getLastSelectedDatabaseId())
        self._updateView()

    def _updateView(self) -> None:
        # if no databases were generated yet show a label.
        if self._currentDatabase is not None:
            self._view.getMenuBar().getSelectAction().setDisabled(False)
            self._view.showDatabase(self._currentDatabase)

        elif self._databaseRepository.count() > 0:
            self._view.getMenuBar().getSelectAction().setDisabled(False)
            self._view.showSelectOrGenerateBox()
            pass

        else:
            self._view.getMenuBar().getSelectAction().setDisabled(True)
            self._view.showNoDatabasesBox()
            return

        # else show the current database.

    def _import(self):
        self._generateOrImport(self._importDatabaseController.run())

    def _generate(self):
        self._generateOrImport(self._generateDatabaseController.run())

    def _generateOrImport(self, databaseId: Optional[Id]):
        if databaseId is None:
            return

        self._setCurrentDatabase(databaseId)
        self._updateView()

    def _differenceIntersect(self) -> None:
        self._differenceIntersectController.run(self._currentDatabase)

    def _search(self):
        self._searchController.run(self._currentDatabase)

    def _update(self):
        self._updateDatabaseController.run(self._currentDatabase)
        self._updateView()

    def _delete(self) -> None:
        result = self._dialogFactory.showConfirmationDialog(
            self._view.tr("Confirm Deletion"),
            self._view.tr(
                "Should the database '{}' really be deleted? This will delete the "
                "database file but leave the corpus and all result files intact."
            ).format(self._currentDatabase.getName()),
            self._view,
            self._view.tr("OK"), self._view.tr("Cancel")
        )

        if not result:
            return

        self._databaseRepository.deleteById(self._currentDatabase.getId())

        try:
            os.remove(str(self._currentDatabase.getPath().asPath()))
        except OSError as e:
            self._logger.info("Database file could not be deleted: {}".format(str(e)))
            self._dialogFactory.showInfoBox(
                self._view.tr("Info"),
                self._view.tr(
                    "The record was deleted but the database file itself could not be deleted. Maybe the file does not "
                    "exist anymore, is not accessible, or currently being used."
                ),
            )

        self._setCurrentDatabase(None)
        self._updateView()

    def _suppliedIntersect(self):
        self._suppliedIntersectController.run(self._currentDatabase, self._view)

    def _setCurrentDatabase(self, id: Optional[Id]) -> None:
        if id is None:
            self._currentDatabase = None
            return

        try:
            self._currentDatabase = self._databaseRepository.findById(id)
            self._runDatabaseCheck()

            self._settings.setLastSelectedDatabaseId(id)
            self._settingsRepository.save(self._settings)

        except DatabaseLoadingException as error:
            self._showDatabaseCouldNotBeLoadedDialog(error)

    def _showDatabaseCouldNotBeLoadedDialog(self, error: DatabaseLoadingException) -> None:
        text = tr(
            "The database '{}' could not be loaded:"
            "\n\n{}\n\n"
            "• Database Name: {}\n"
            "• Database Path: {}\n"
            "• Corpus Path: {}"
            .format(error.getName(), str(error), error.getName(), error.getPath(), error.getCorpusPath())
        )

        result = self._dialogFactory.showConfirmationDialog(
            tr("Database could not be loaded"),
            text,
            self._view,
            tr("Delete Database"),
            tr("Cancel"),
            icon=QMessageBox.Warning,
            details=error.getDetails()
        )

        if result:
            self._databaseRepository.deleteByDatabasePath(error.getPath())

        self._setCurrentDatabase(None)
        self._updateView()

    def _runDatabaseCheck(self) -> None:
        if self._currentDatabase is None:
            return

        runnable = CheckDatabaseRunnable(self._currentDatabase)
        progressDialog = self._dialogFactory.showProgressDialog(
            self._view,
            tr("Checking Database/Corpus"),
            0,  # indeterminate,
            tr("Checking database-corpus match. Please be patient.") + "...",
            runnable
        )
        progressDialog.canceled.connect(runnable.cancel)

        runnable.getSignals().getFinishedSignal().connect(lambda: self._checkWitnessReport(runnable, progressDialog))

        self._qThreadPool.start(runnable)

    def _checkWitnessReport(self, runnable: CheckDatabaseRunnable, progressDialog: QProgressDialog) -> None:
        progressDialog.close()
        report = runnable.getReport()

        if report is None or runnable.isCancelled():
            return

        if report.hasChangedOrAddedWitnesses() or report.hasMissingWitnesses():
            result = self._dialogFactory.showConfirmationDialog(
                tr("Update Database?"),
                tr(
                    "The corpus does not match the database. Some works/witnesses have been "
                    "modified, were newly added, or have been removed. See \"Show Details\" "
                    "for a list of witnesses. "
                    "Do you want to update the database?"
                ),
                self._view,
                tr("Update"),
                tr("Cancel"),
                details=report.createReportText()
            )

            if result:
                self._taclRunner.runNgrams(
                    self._currentDatabase.getPath(),
                    self._currentDatabase.getCorpusPath(),
                    self._currentDatabase.getNGramLengths(),
                    self._view,
                    tr("Updating n-grams Database"),
                    lambda: None
                )

    def _select(self) -> None:
        currentDatabaseId = None
        if self._currentDatabase is not None:
            currentDatabaseId = self._currentDatabase.getId()

        selectedId = self._selectDatabaseController.run(currentDatabaseId)

        if selectedId is not None:
            self._setCurrentDatabase(selectedId)
            self._updateView()

    def _exit(self):
        self._view.close()

    def _filterRationalise(self):
        self._filterRationaliseController.run(self._currentDatabase)
