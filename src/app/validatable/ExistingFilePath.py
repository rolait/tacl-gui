import os

from app.utils import tr

from app.validatable.FilePath import FilePath
from app.inputValidator.ValidationError import ValidationError


class ExistingFilePath(FilePath):

    def __init__(self, pathString: str, pathName: str, dirPath: bool):
        super().__init__(pathString, pathName, dirPath)

        if not self._path.exists():
            raise ValidationError(tr("The {} does not exist.").format(pathName))

        if not os.access(str(self._path), os.R_OK):
            raise ValidationError(tr(
                "The {} can not be accessed "
                "(maybe due to insufficient permissions)."
            ).format(pathName))