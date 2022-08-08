import os
from unittest.mock import patch

from app.inputValidator.ValidationError import ValidationError
from app.validatable.CorpusPath import CorpusPath
from app.validatable.DatabaseName import DatabaseName
from test.TaclGuiTestCase import TaclGuiTestCase


class DatabaseNameTest(TaclGuiTestCase):

    def test_init_throwsErrorWhenNameIsEmpty(self):
        self.assertRaises(ValidationError, lambda: DatabaseName(""))

    def test_init_throwsValidationErrorWhenTrimmedNameIsEmpty(self):
        self.assertRaises(ValidationError, lambda: DatabaseName("  "))

    def test_init_returnsObjectWhenValidName(self):
        dbName = DatabaseName("test")

        self.assertEqual("test", str(dbName))




