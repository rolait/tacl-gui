from app.utils import tr
from app.validatable.NonEmptyString import NonEmptyString

from app.validatable.ValidatableObject import ValidatableObject
from app.inputValidator.ValidationError import ValidationError


class DatabaseName(NonEmptyString):
    def __init__(self, value: str):
        super().__init__("database name", value)
