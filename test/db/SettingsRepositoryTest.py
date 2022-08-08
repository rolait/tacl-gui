from unittest.mock import Mock, MagicMock

from app.Database import Database
from app.ResultType import ResultType
from app.Settings import Settings
from app.repositories.ResultRepository import ResultRepository
from app.repositories.SettingsRepository import SettingsRepository
from app.validatable.Id import Id
from app.validatable.ResultPath import ResultPath
from test.TaclGuiDbTestCase import TaclGuiDbTestCase


class SettingsRepositoryTest(TaclGuiDbTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._repo = SettingsRepository(self.getConnection())

    def test_find_returnsSettingsIfExistent(self):
        self._populateData()

        settings = self._repo.find()
        self.assertEqual(2, settings.getLastSelectedDatabaseId().asInt())
        self.assertEqual('openPath', settings.getLastOpenPath())
        self.assertEqual('savePath', settings.getLastSavePath())

    def test_find_returnsDefaultSettingsIfNotExistent(self):

        settings = self._repo.find()
        self.assertIsNone(settings.getLastSelectedDatabaseId())
        self.assertEqual('', settings.getLastOpenPath())
        self.assertEqual('', settings.getLastSavePath())

    def test_save_updatesSettings(self):
        self._populateData()
        self._repo.save(Settings(Id(1), 'openPath2', 'savePath2'))

        settings = self._repo.find()

        self.assertEqual(1, settings.getLastSelectedDatabaseId().asInt())
        self.assertEqual('openPath2', settings.getLastOpenPath())
        self.assertEqual('savePath2', settings.getLastSavePath())

    def _populateData(self):
        self.executeUpdate("INSERT INTO settings VALUES (2, 'openPath', 'savePath')")