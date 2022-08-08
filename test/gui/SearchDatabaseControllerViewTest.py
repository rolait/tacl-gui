import sys
from tempfile import NamedTemporaryFile
from unittest.mock import Mock, MagicMock, patch

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from app.Database import Database
from app.controllers.SearchController import SearchController
from app.controllers.UpdateDatabaseController import UpdateDatabaseController
from app.inputValidator.InputValidator import InputValidator
from app.inputValidator.InputValidatorFactory import InputValidatorFactory
from app.repositories.DatabaseRepository import DatabaseRepository
from app.tacl.TaclRunner import TaclRunner
from app.validatable.CorpusPath import CorpusPath
from app.validatable.DatabaseNGramLengths import DatabaseNGramLengths
from app.validatable.DatabaseName import DatabaseName
from app.validatable.DatabasePath import DatabasePath
from app.validatable.Id import Id
from app.views.DialogFactory import DialogFactory
from app.views.MainView import QApplication
from app.views.SearchView import SearchView
from app.views.UpdateDatabaseView import UpdateDatabaseView
from test.TaclGuiTestCase import TaclGuiTestCase

app = QApplication(sys.argv)


class SearchDatabaseControllerViewTest(TaclGuiTestCase):

    def setUp(self) -> None:
        self._dialogFactory: DialogFactory = Mock(spec=DialogFactory)
        self._view = SearchView(self._dialogFactory)
        self._inputValidatorFactory: InputValidatorFactory = Mock(spec=InputValidatorFactory)
        self._taclRunner: TaclRunner = Mock(spec=TaclRunner)
        self._inputValidator: InputValidator = Mock(spec=InputValidator)
        self._inputValidatorFactory.getInputValidator = MagicMock(return_value=self._inputValidator)

        self._controller = SearchController(
            self._view,
            self._inputValidatorFactory,
            self._taclRunner,
            self._dialogFactory,
        )

        self._database = Database(
            Id(1),
            DatabaseName("Test"), DatabasePath(self.resource("test.db")),
            CorpusPath(self.resource("db/corpus")), DatabaseNGramLengths(2, 3)
        )
        self._view.showAsApplicationModal = MagicMock()
        self._controller.run(self._database)

    def test_search_doesNotRunCommandIfInputInvalid(self):
        self._inputValidator.showErrorDialog = MagicMock(return_value=True)
        QTest.mouseClick(self._view.getRunTestButton(), Qt.LeftButton)
        self._taclRunner.runNgrams().assert_not_called()

    def test_cancel_dialogueIsClosed(self):
        self._view.setVisible(True)
        QTest.mouseClick(self._view.getCancelButton(), Qt.LeftButton)
        self.assertFalse(self._view.isVisible())

    def test_search_runsCommandIfInputValid(self):
        self._runSearch()
        self._taclRunner.runSearch.assert_called_once()

    def _runSearch(self):
        self._inputValidator.showErrorDialog = MagicMock(return_value=False)
        self._taclRunner.runNgrams = MagicMock(
            side_effect=lambda d, c, n, o, g, v, cb: cb()
        )
        QTest.mouseClick(self._view.getRunTestButton(), Qt.LeftButton)
