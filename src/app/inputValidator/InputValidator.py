from typing import List, Callable, Optional

from app.validatable.ValidatableObject import ValidatableObject
from app.views.DialogFactory import DialogFactory
from app.inputValidator.ValidationError import ValidationError


class InputValidator:

    _ERROR_LIST_ITEM_SUFFIX = "• "

    def __init__(self, dialogFactory: DialogFactory):
        self._dialogFactory = dialogFactory
        self._errors: List[str] = []
        self._details = None

    def validate(self, validateFunction: Callable[[], ValidatableObject]) -> Optional[ValidatableObject]:
        """
        Tries to instantiate a validatable object and collects error messages.

        :param validateFunction: A callable which returns a ValidatableObject.
        :return: None, if the ValidatableObject was invalid. Else the instantiated ValidatableObject.
        """

        try:
            result = validateFunction()

        except ValidationError as validationError:
            self.addError(str(validationError))
            return None

        return result

    def addError(self, errorMsg: str, details: str = None) -> None:
        self._errors.append(self._ERROR_LIST_ITEM_SUFFIX + errorMsg)
        
        if details is not None:
            self._details = details

    def showErrorDialog(self) -> bool:
        """
        In case there are errors this method shows a dialog listing the input errors.
        :return: true, if the error dialog was shown.
        """

        if len(self._errors) == 0:
            return False

        # show only the first ten errors
        if len(self._errors) <= 10:
            message = '\n'.join(self._errors)
        else:
            message = '\n'.join(self._errors[0:9])
            message += "\n[...]"

        self._dialogFactory.showInputError(message, self._details)

        return True

    def getErrors(self) -> List[str]:
        return self._errors