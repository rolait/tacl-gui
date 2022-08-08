from app.inputValidator.ValidationError import ValidationError


class DatabaseNGramLengths:

    def __init__(self, minLength: int, maxLength: int):
        if minLength < 2:
            raise ValidationError("The n-gram min length must be > 2: {}".format(minLength))

        if minLength > maxLength:
            raise ValidationError(
                "The n-gram max length must be greater than the min length (min/max): {}/{}"
                .format(minLength, maxLength)
            )

        self._minLength = minLength
        self._maxLength = maxLength

    def getMinLength(self) -> int:
        return self._minLength

    def getMaxLength(self) -> int:
        return self._maxLength
