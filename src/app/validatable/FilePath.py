from pathlib import Path

from app.utils import tr

from app.validatable.ValidatableObject import ValidatableObject
from app.inputValidator.ValidationError import ValidationError


class FilePath(ValidatableObject):
    _TRUNCATED_PART = "..."

    def __init__(self, pathString: str, pathName: str, dirPath: bool):
        super().__init__()

        pathString = pathString.strip()

        if not pathString:
            raise ValidationError(tr("The {} must not be empty.").format(pathName))

        path = Path(pathString).absolute()

        if path.exists():
            if dirPath and path.is_file():
                raise ValidationError(tr("The {} must be a directory.").format(pathName))
            elif not dirPath and path.is_dir():
                raise ValidationError(tr("The {} must not be a directory.").format(pathName))

        self._path: Path = path

    def asPath(self) -> Path:
        return self._path

    def truncate(self, maxLength: int) -> str:
        if maxLength < 25:
            raise ValidationError("Max length must be >= 25: {}".format(maxLength))

        if len(str(self._path)) <= maxLength:
            return str(self._path)

        truncatedPathStart = Path("")
        partsCount = len(self._path.parts)

        # keep first part if is not too long (e.g. "/" or "c:\\")
        firstPart = self._path.parts[0]
        if partsCount > 1 and len(firstPart) <= 5:
            truncatedPathStart = truncatedPathStart.joinpath(firstPart)

        # try to truncate middle part if there is any and if it is too long.
        if partsCount > 2:
            for i in range (1, partsCount):
                remainderPart = str(Path(*self._path.parts[i:]))
                truncatedPath = str(truncatedPathStart.joinpath(self._TRUNCATED_PART).joinpath(remainderPart))

                if len(truncatedPath) <= maxLength:
                    return truncatedPath

            if partsCount == 3 and len(self._path.parts[1]) <= 5:
                truncatedPathStart = truncatedPathStart.joinpath(self._path.parts[1])
            else:
                truncatedPathStart = truncatedPathStart.joinpath(self._TRUNCATED_PART)

        # truncate file name
        name = self._path.name
        remainderLength = maxLength - (5 + len(self._TRUNCATED_PART) + len(str(truncatedPathStart)))
        truncatedFileName = name[:5] + self._TRUNCATED_PART + name[-remainderLength:]

        return str(truncatedPathStart.joinpath(truncatedFileName))

    def __str__(self):
        return str(self._path)
