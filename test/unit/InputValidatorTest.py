from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from app.inputValidator.ValidationError import ValidationError
from app.inputValidator.InputValidator import InputValidator
from app.validatable.ValidatableObject import ValidatableObject
from app.views.DialogFactory import DialogFactory


class InputValidatorTest(TestCase):

    def setUp(self) -> None:
        self._dialogFactory: DialogFactory | Mock = Mock(spec=DialogFactory)

    def test_validate_addsAndShowsErrorsWhenInvalid(self):
        validator = InputValidator(self._dialogFactory)
        returnValue = validator.validate(self._validateFunctionWithError)

        self.assertEqual(None, returnValue)
        self.assertEqual(1, len(validator.getErrors()))
        self.assertTrue("test error" in validator.getErrors()[0])

        validator.showErrorDialog()
        self.assertTrue(self._dialogFactory.showInputError.called)

    def test_validate_addsNoErrorWhenValid(self):
        validator = InputValidator(self._dialogFactory)

        object: ValidatableObject = Mock(spec=ValidatableObject)
        returnValue = validator.validate(lambda: object)

        self.assertEqual(object, returnValue)
        self.assertFalse(validator.showErrorDialog())

    def _validateFunctionWithError(self):
        raise ValidationError("test error")
