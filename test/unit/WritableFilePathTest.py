import os
from unittest.mock import patch

from app.inputValidator.ValidationError import ValidationError
from app.validatable.WritableFilePath import WritableFilePath
from test.TaclGuiTestCase import TaclGuiTestCase


def noWriteAccess(path: str, mode: int) -> bool:
    if mode == os.W_OK:
        return False


def writeAccess(path: str, mode: int) -> bool:
    return True


@patch("app.validatable.WritableFilePath.tr", side_effect = lambda text: text)
class WritableFilePathTest(TaclGuiTestCase):

    @patch("app.validatable.WritableFilePath.os.access", side_effect=noWriteAccess)
    def test_init_throwsValidationErrorWhenFileNotWritable(self, access, tr):
        self.assertRaises(
            ValidationError,
            lambda: WritableFilePath(self.RESOURCE_DIR + "WritableFilePathTest/file", "test")
        )

    @patch("app.validatable.WritableFilePath.os.access", side_effect=writeAccess)
    def test_init_returnsObjectWhenWritable(self, access, tr):
        path = str(os.path.abspath(self.RESOURCE_DIR + "WritableFilePathTest/file"))
        writablePath = WritableFilePath(path, "test")
        self.assertEqual(path, str(writablePath))

