from app.inputValidator.ValidationError import ValidationError
from app.validatable.ValidatableObject import ValidatableObject


class Id(ValidatableObject):

    def __init__(self, id: int):
        if id is None or id <= 0:
            raise ValidationError("The id must be > 0: {}".format(id))

        self._id = id

    def asInt(self) -> int:
        return self._id

    def __eq__(self, other):
        return isinstance(other, Id) and other.asInt() == self._id

    def __hash__(self):
        return self._id