import os
import sys
from logging import Logger
from typing import Optional
from unittest.mock import Mock, MagicMock

from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtTest import QTest

from app.Database import Database
from app.DatabaseLoadingException import DatabaseLoadingException
from app.Settings import Settings
from app.controllers.DifferenceIntersectController import DifferenceIntersectController
from app.controllers.FilterRationaliseController import FilterRationaliseController
from app.controllers.GenerateDatabaseController import GenerateDatabaseController
from app.controllers.ImportDatabaseController import ImportDatabaseController
from app.controllers.MainController import MainController
from app.controllers.SearchController import SearchController
from app.controllers.SelectDatabaseController import SelectDatabaseController
from app.controllers.SuppliedIntersectController import SuppliedIntersectController
from app.controllers.UpdateDatabaseController import UpdateDatabaseController
from app.repositories.DatabaseRepository import DatabaseRepository
from app.repositories.SettingsRepository import SettingsRepository
from app.tacl.TaclRunner import TaclRunner
from app.validatable.CorpusPath import CorpusPath
from app.validatable.DatabaseNGramLengths import DatabaseNGramLengths
from app.validatable.DatabaseName import DatabaseName
from app.validatable.DatabasePath import DatabasePath
from app.validatable.Id import Id
from app.views.DialogFactory import DialogFactory
from app.views.MainView import MainView, QApplication
from test.TaclGuiTestCase import TaclGuiTestCase

app = QApplication(sys.argv)

class MainControllerViewTest(TaclGuiTestCase):

    def setUp(self) -> None:
        self._dbPath = self.resource("MainControllerViewTest/test.db")
        open(self._dbPath, 'a').close()

    def tearDown(self) -> None:
        if os.path.exists(self._dbPath):
            os.remove(self._dbPath)

    def test_run_noDatabaseBoxIsShownWhenNoDatabasesGeneratedYet(self):
        self._runController(None, 0)

        self.assertTrue(self._view.getNoDatabaseBox().isVisible())
        self.assertFalse(self._view.getSelectOrGenerateDatabaseBox().isVisible())
        self.assertFalse(self._view.getDatabaseInfoBox().isVisible())

    def test_run_selectOrGenerateDAtabseBoxIsShownWhenNoDatabaseSelected(self):
        self._runController(None, 1)

        self.assertFalse(self._view.getNoDatabaseBox().isVisible())
        self.assertTrue(self._view.getSelectOrGenerateDatabaseBox().isVisible())
        self.assertFalse(self._view.getDatabaseInfoBox().isVisible())

    def test_run_databaseInfoBoxIsShownWhenDatabaseSelected(self):
        self._runController(Id(1), 1)

        self.assertFalse(self._view.getNoDatabaseBox().isVisible())
        self.assertFalse(self._view.getSelectOrGenerateDatabaseBox().isVisible())
        self.assertTrue(self._view.getDatabaseInfoBox().isVisible())

    def test_generate_showsNewDatabaseAfterGeneration(self):
        self._runController(None, 0)

        self._generateDatabaseController.run = MagicMock(return_value=Id(1))

        QTest.mouseClick(self._view.getNoDatabaseBox().getGenerateButton(), Qt.LeftButton)

        self._generateDatabaseController.run.assert_called_once()

        self.assertFalse(self._view.getNoDatabaseBox().isVisible())
        self.assertFalse(self._view.getSelectOrGenerateDatabaseBox().isVisible())
        self.assertTrue(self._view.getDatabaseInfoBox().isVisible())

    def test_generate_showsNoDatabaseWhenGenerationCancelled(self):
        self._runController(None, 0)

        QTest.mouseClick(self._view.getNoDatabaseBox().getGenerateButton(), Qt.LeftButton)

        self._generateDatabaseController.run.assert_called_once()

        self.assertTrue(self._view.getNoDatabaseBox().isVisible())
        self.assertFalse(self._view.getSelectOrGenerateDatabaseBox().isVisible())
        self.assertFalse(self._view.getDatabaseInfoBox().isVisible())

    def test_delete_deletesFromDatabaseAndDeletesFile(self):
        self._runController(Id(1), 1)

        self._dialogFactory.showConfirmationDialog = MagicMock(return_value=True)

        QTest.mouseClick(self._view.getDatabaseInfoBox().getDeleteButton(), Qt.LeftButton)

        self._databaseRepository.deleteById.assert_called_once_with(Id(1))
        self._dialogFactory.showInfoBox.assert_not_called()
        self.assertFalse(os.path.exists(self._dbPath))

    def test_delete_showsInfoBoxWhenDatabaseCouldNotBeDeleted(self):
        self._runController(Id(1), 1)

        os.remove(self._dbPath)
        self._dialogFactory.showConfirmationDialog = MagicMock(return_value=True)

        QTest.mouseClick(self._view.getDatabaseInfoBox().getDeleteButton(), Qt.LeftButton)

        self._databaseRepository.deleteById.assert_called_once_with(Id(1))
        self._dialogFactory.showInfoBox.assert_called_once()

    def test_select_showsSelectedDatabase(self):
        self._runController(None, 1)
        self._selectDatabaseController.run = MagicMock(return_value=Id(1))

        self.assertTrue(self._view.getSelectOrGenerateDatabaseBox().isVisible())

        QTest.mouseClick(self._view.getSelectOrGenerateDatabaseBox().getSelectButton(), Qt.LeftButton)

        self._selectDatabaseController.run.assert_called_once()
        self.assertTrue(self._view.getDatabaseInfoBox().isVisible())

    def test_select_showsNoDatabaseIfCancelledAndNoDatabasePreviouslySelected(self):
        self._runController(None, 1)
        self._selectDatabaseController.run = MagicMock(return_value=None)


        self.assertTrue(self._view.getSelectOrGenerateDatabaseBox().isVisible())

        QTest.mouseClick(self._view.getSelectOrGenerateDatabaseBox().getSelectButton(), Qt.LeftButton)

        self._selectDatabaseController.run.assert_called_once()
        self.assertTrue(self._view.getSelectOrGenerateDatabaseBox().isVisible())

    def test_select_showsPreviouslySelectedDatbaseIfCancelled(self):
        self._runController(Id(1), 1)
        self._selectDatabaseController.run = MagicMock(return_value=Id(1))

        self.assertTrue(self._view.getDatabaseInfoBox().isVisible())

        QTest.mouseClick(self._view.getSelectOrGenerateDatabaseBox().getSelectButton(), Qt.LeftButton)

        self._selectDatabaseController.run.assert_called_once()
        self.assertTrue(self._view.getDatabaseInfoBox().isVisible())

    def test_delete_databaseNotDeletedWhenCanceled(self):
        self._runController(Id(1), 1)

        self._dialogFactory.showConfirmationDialog = MagicMock(return_value=False)

        QTest.mouseClick(self._view.getDatabaseInfoBox().getDeleteButton(), Qt.LeftButton)

        self._databaseRepository.deleteById.assert_not_called()
        self._dialogFactory.showInfoBox.assert_not_called()
        self.assertTrue(os.path.exists(self._dbPath))

    def test_differenceIntersect_ControllerIsRun(self):
        self._runController(None, 0)

        QTest.mouseClick(self._view.getDifferenceIntersectButton(), Qt.LeftButton)
        self._differenceIntersectController.run.assert_called_once()

    def test_search_ControllerIsRun(self):
        self._runController(None, 0)

        QTest.mouseClick(self._view.getSearchButton(), Qt.LeftButton)
        self._searchController.run.assert_called_once()

    def test_update_ControllerIsRun(self):
        self._runController(None, 0)

        QTest.mouseClick(self._view.getDatabaseInfoBox().getUpdateButton(), Qt.LeftButton)
        self._updateDatabaseController.run.assert_called_once()

    def test_suppliedIntersect_intersectControllerRun(self):
        self._runController(None, 0)

        QTest.mouseClick(self._view.getSuppliedIntersectButton(), Qt.LeftButton)
        self._suppliedIntersectController.run.assert_called_once()

    def test_import_importControllerRunWhenClickedFromMenu(self):
        self._runController(None, 0)

        self._view.getMenuBar().getImportAction().trigger()
        self._importDatabaseController.run.assert_called_once()

    def _runController(self, lastDatabaseId: Optional[Id], databaseCount: int) -> None:
        self._view = MainView(QApplication.desktop())
        self._databaseRepository: DatabaseRepository = Mock(spec=DatabaseRepository)
        self._generateDatabaseController: GenerateDatabaseController = Mock(spec=GenerateDatabaseController)
        self._importDatabaseController: ImportDatabaseController = Mock(spec=ImportDatabaseController)
        self._updateDatabaseController: UpdateDatabaseController = Mock(spec=UpdateDatabaseController)
        self._differenceIntersectController = Mock(spec=DifferenceIntersectController)
        self._searchController = Mock(spec=SearchController)
        self._logger = Mock(spec=Logger)
        self._settingsRepository = Mock(spec=SettingsRepository)
        self._dialogFactory: DialogFactory = Mock(spec=DialogFactory)
        self._selectDatabaseController = Mock(spec=SelectDatabaseController)
        self._suppliedIntersectController = Mock(spec=SuppliedIntersectController)
        self._filterRationaliseController: FilterRationaliseController = Mock(spec=FilterRationaliseController)
        self._taclRunner: TaclRunner = Mock(spec=TaclRunner)
        self._qThreadPool: QThreadPool = Mock(spec=QThreadPool)

        self._settings: Settings = Mock(spec=Settings)
        self._settingsRepository.find = MagicMock(return_value=self._settings)
        self._settings.getLastSelectedDatabaseId = MagicMock(return_value=lastDatabaseId)

        self._databaseRepository.count = MagicMock(return_value=databaseCount)
        self._databaseRepository.findById = MagicMock(side_effect=self._databaseRepository_FindById)

        self._controller = MainController(
            self._view,
            self._databaseRepository,
            self._generateDatabaseController,
            self._importDatabaseController,
            self._updateDatabaseController,
            self._differenceIntersectController,
            self._searchController,
            self._logger,
            self._settingsRepository,
            self._dialogFactory,
            self._selectDatabaseController,
            self._suppliedIntersectController,
            self._filterRationaliseController,
            self._taclRunner,
            self._qThreadPool
        )

        self._controller._runDatabaseCheck = MagicMock(side_effect=lambda: None)
        self._controller.run()

    def _throwDatabaseLoadingException(self):
        raise DatabaseLoadingException();

    def _databaseRepository_FindById(self, id: Id):
        if id.asInt() == 1:
            return Database(
                id,
                DatabaseName("Test Database"),
                DatabasePath(self._dbPath),
                CorpusPath(self.resource("db/corpus")),
                DatabaseNGramLengths(2, 3)
            )

        return None