from app.utils import tr

from app.validatable.ValidatableObject import ValidatableObject
from app.inputValidator.ValidationError import ValidationError


class NonEmptyString(ValidatableObject):

    def __init__(self, name: str, value: str):
        super().__init__()

        value = value.strip()

        if len(value) == 0:
            raise ValidationError(tr(f"The {name} must not be empty."))

        self._value = value

    def __str__(self):
        return self._value
