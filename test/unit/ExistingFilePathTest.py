import os
from unittest.mock import patch

from app.inputValidator.ValidationError import ValidationError
from app.validatable.ExistingFilePath import ExistingFilePath
from test.TaclGuiTestCase import TaclGuiTestCase


def noReadAccess(path: str, mode: int) -> bool:
    if mode == os.R_OK:
        return False


def readAccess(path: str, mode: int) -> bool:
    return True


@patch("app.validatable.ExistingFilePath.tr", side_effect = lambda text: text)
class ExistingFilePathTest(TaclGuiTestCase):

    def test_init_throwsValidationErrorWhenPathDoesNotExist(self, tr):
        self.assertRaises(
            ValidationError,
            lambda: ExistingFilePath(self.RESOURCE_DIR + "ExistingFilePathTest/notExistingFile", "test", False)
        )

    @patch("app.validatable.ExistingFilePath.os.access", side_effect=noReadAccess)
    def test_init_throwsValidationErrorWhenPathIsNotAccessible(self, tr, osAccess):
        self.assertRaises(
            ValidationError,
            lambda: ExistingFilePath(self.RESOURCE_DIR + "ExistingFilePathTest/existingFile", "test", False)
        )

    @patch("app.validatable.ExistingFilePath.os.access", side_effect=readAccess)
    def test_init_returnsObjectForExistingFile(self, tr, osAccess):
        path = self.RESOURCE_DIR + "ExistingFilePathTest/existingFile"
        existingPath = ExistingFilePath(path, "test", False)

        self.assertEqual(path, str(existingPath))

