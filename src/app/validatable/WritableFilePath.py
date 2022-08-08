import os

from app.utils import tr
from app.validatable.FilePath import FilePath
from app.inputValidator.ValidationError import ValidationError


class WritableFilePath(FilePath):

    def __init__(self, pathString: str, pathName: str):
        super().__init__(pathString, pathName, False)

        if self._path.exists() and not os.access(str(self._path), os.W_OK):
            raise ValidationError(tr(
                "The {} can not be accessed "
                "(maybe due to insufficient permissions)."
            ).format(pathName))