from app.inputValidator.ValidationError import ValidationError
from app.validatable.Id import Id
from test.TaclGuiTestCase import TaclGuiTestCase


class IdTest(TaclGuiTestCase):

    def test_init_throwsErrorForNonPositiveId(self):
        self.assertRaises(ValidationError, lambda: Id(-1))
        self.assertRaises(ValidationError, lambda: Id(0))

    def test_init_returnsObjectWhenValidName(self):
        id = Id(1)

        self.assertEqual(1, id.asInt())




