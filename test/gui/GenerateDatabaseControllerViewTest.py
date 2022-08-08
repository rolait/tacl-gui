import sys
from unittest.mock import Mock, MagicMock, patch

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from app.controllers.GenerateDatabaseController import GenerateDatabaseController
from app.inputValidator.InputValidator import InputValidator
from app.inputValidator.InputValidatorFactory import InputValidatorFactory
from app.repositories.DatabaseRepository import DatabaseRepository
from app.tacl.TaclRunner import TaclRunner
from app.validatable.NewDatabasePath import NewDatabasePath
from app.views.DialogFactory import DialogFactory
from app.views.GenerateDatabaseView import GenerateDatabaseView
from app.views.MainView import QApplication
from test.TaclGuiTestCase import TaclGuiTestCase

app = QApplication(sys.argv)
unlink = Mock()


class GenerateDatabaseControllerViewTest(TaclGuiTestCase):

    def setUp(self) -> None:
        self._dialogFactory: DialogFactory = Mock(spec=DialogFactory)
        self._view = GenerateDatabaseView(self._dialogFactory)
        self._inputValidatorFactory: InputValidatorFactory = Mock(spec=InputValidatorFactory)
        self._databaseRepository: DatabaseRepository = Mock(spec=DatabaseRepository)
        self._taclRunner: TaclRunner = Mock(spec=TaclRunner)
        self._inputValidator: InputValidator = Mock(spec=InputValidator)

        self._inputValidatorFactory.getInputValidator = MagicMock(return_value=self._inputValidator)

        self._controller = GenerateDatabaseController(
            self._view,
            self._dialogFactory,
            self._inputValidatorFactory,
            self._databaseRepository,
            self._taclRunner
        )

    def test_create_doesNotRunNgramsCommandIfInputInvalid(self):
        self._inputValidator.showErrorDialog = MagicMock(return_value=True)

        QTest.mouseClick(self._view.getGenerateButton(), Qt.LeftButton)

        self._taclRunner.runNgrams.assert_not_called()

    @patch("app.controllers.GenerateDatabaseController.os.unlink", side_effect=lambda path: unlink())
    def test_create_runsNgramsCommandIfInputValid(self, unlink):
        self._inputValidator.showErrorDialog = MagicMock(return_value=False)
        self._taclRunner.runNgrams = MagicMock(
            side_effect=lambda p, c, n, v, t, callable: callable()
        )

        QTest.mouseClick(self._view.getGenerateButton(), Qt.LeftButton)

        self._taclRunner.runNgrams.assert_called_once()
        self._databaseRepository.deleteByDatabasePath.assert_called_once()
        self._databaseRepository.save.assert_called_once()

    @patch("app.controllers.GenerateDatabaseController.os.unlink", side_effect=lambda path: unlink(path))
    def test_create_doesNotRunCommandWhenFileExistsAndOverwriteDenied(self, unlink):
        self._inputValidator.showErrorDialog = MagicMock(return_value=False)
        self._dialogFactory.showOverwriteDialogIfFileExistent = MagicMock(return_value=False)

        QTest.mouseClick(self._view.getGenerateButton(), Qt.LeftButton)

        self._taclRunner.runNgrams.assert_not_called()

    @patch("app.controllers.GenerateDatabaseController.os.unlink", side_effect=lambda path: unlink(path))
    def test_create_deletesFileWhenOverwriteAccepted(self, unlink):
        self._inputValidator.showErrorDialog = MagicMock(return_value=False)
        self._dialogFactory.showOverwriteDialogIfFileExistent = MagicMock(return_value=True)
        self._inputValidator.validate = MagicMock(return_value=NewDatabasePath(self.resource("test.db")))

        QTest.mouseClick(self._view.getGenerateButton(), Qt.LeftButton)
        unlink.assert_called_once()

