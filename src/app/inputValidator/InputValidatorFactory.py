from app.views.DialogFactory import DialogFactory
from app.inputValidator.InputValidator import InputValidator


class InputValidatorFactory:

    def __init__(self, dialogFactory: DialogFactory):
        self._dialogFactory = dialogFactory

    def getInputValidator(self) -> InputValidator:
        return InputValidator(self._dialogFactory)
