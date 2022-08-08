from unittest import TestCase

from app.inputValidator.ValidationError import ValidationError
from app.validatable.DatabaseNGramLengths import DatabaseNGramLengths


class DatabaseNGramLengthsTest(TestCase):

    def test_init_throwsErrorWhenMinLengthLessThan2(self):
        self.assertRaises(ValidationError, lambda: DatabaseNGramLengths(1, 2))

    def test_init_throwsErrorWhenMinGreaterThanMax(self):
        self.assertRaises(ValidationError, lambda: DatabaseNGramLengths(3, 2))

    def test_init_valuesAreCorrectlySet(self):
        d = DatabaseNGramLengths(2, 3)
        self.assertEqual(2, d.getMinLength())
        self.assertEqual(3, d.getMaxLength())
