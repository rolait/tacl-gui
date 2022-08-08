import os
from unittest.mock import patch

from app.inputValidator.ValidationError import ValidationError
from app.validatable.FilePath import FilePath
from test.TaclGuiTestCase import TaclGuiTestCase


@patch("app.validatable.FilePath.tr", return_value="test")
class FilePathTest(TaclGuiTestCase):

    def test_init_throwsValidationErrorWhenPathIsEmpty(self, tr):
        self.assertRaises(
            ValidationError,
            lambda: FilePath("", "test", False)
        )

    def test_init_throwsValidationWhenPathIsDirButShouldBeFile(self, tr):
        self.assertRaises(
            ValidationError,
            lambda: FilePath(self.RESOURCE_DIR + "FilePathTest/dir", "test", False)
        )

    def test_init_throwsValidationWhenPathIsFileButShouldBeDir(self, tr):
        self.assertRaises(
            ValidationError,
            lambda: FilePath(self.RESOURCE_DIR + "FilePathTest/file", "test", True)
        )

    def test_init_returnsObjectForFile(self, tr):
        path = str(os.path.abspath(self.RESOURCE_DIR + "FilePathTest/file"))
        filePath = FilePath(path, "test", False)

        self.assertEqual(path, str(filePath))

    def test_init_returnsObjectForDir(self, tr):
        path = str(os.path.abspath(self.RESOURCE_DIR + "FilePathTest/dir"))
        filePath = FilePath(path, "test", True)

        self.assertEqual(path, str(filePath))

    def test_truncate_throwsErrorWhenMaxLengthTooLow(self, tr):
        filePath = FilePath("some/file.txt", "test", False)
        self.assertRaises(ValidationError, lambda: filePath.truncate(-1))
        self.assertRaises(ValidationError, lambda: filePath.truncate(0))
        self.assertRaises(ValidationError, lambda: filePath.truncate(10))
        self.assertRaises(ValidationError, lambda: filePath.truncate(24))

    def test_truncate_doesNotTruncatePathWhenMaxLengthGreaterThanPathLength(self, tr):
        path = str(os.path.abspath("/some/file.txt"))
        self.assertEqual(path, FilePath(path, "test", False).truncate(25))

    def test_truncate_truncatesVeryLongFileName(self, tr):
        path = "/123456789012345678901234567890.txt"
        truncatedPath = FilePath(path, "test", False).truncate(25)

        self.assertEqual("/12345...901234567890.txt", truncatedPath)

    def test_truncate_truncatesLongDirectoryName(self, tr):
        path = "/123456789012345678901234567890/some/path/file.txt"
        truncatedPath = FilePath(path, "test", False).truncate(25)

        self.assertEqual("/.../some/path/file.txt", truncatedPath)
