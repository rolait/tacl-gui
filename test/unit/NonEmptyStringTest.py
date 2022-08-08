from app.inputValidator.ValidationError import ValidationError
from app.validatable.Id import Id
from app.validatable.NonEmptyString import NonEmptyString
from test.TaclGuiTestCase import TaclGuiTestCase


class NonEmptyStringTest(TaclGuiTestCase):

    def test_init_throwsErrorForEmptyString(self):
        self.assertRaises(ValidationError, lambda: NonEmptyString("test string", ""))

    def test_init_returnsObjectWhenNotEmptyString(self):
        string = NonEmptyString("test string", "test")

        self.assertEqual("test", str(string))




