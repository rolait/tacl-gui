import os
from tempfile import TemporaryFile, NamedTemporaryFile

from app.utils import tr

from app.validatable.ExistingFilePath import ExistingFilePath
from app.inputValidator.ValidationError import ValidationError


class CorpusPath(ExistingFilePath):

    DEFAULT_LABEL = "DefaultLabel"

    def __init__(self, pathString: str):
        super().__init__(pathString, tr("corpus path"), True)

        workCount: int = self._countWorks(str(self._path))
        if workCount == 0:
            raise ValidationError(tr("The corpus path does not seem to contain any works"))

        self._workCount: int = workCount

    def _countWorks(self, path: str):
        workCount: int = 0

        # Count the sub-directories
        for file in os.listdir(path):
            if os.path.isdir(os.path.join(path, file)):
                workCount += 1

        return workCount

    def createBaseCatalogueFile(self) -> TemporaryFile:
        catalogueFile = NamedTemporaryFile(mode="w+", delete=False, encoding='utf-8')

        dirList = os.listdir(str(self._path))
        dirList.sort()

        for work in dirList:
            line = work + " " + self.DEFAULT_LABEL + "\n"
            catalogueFile.write(line)

        catalogueFile.flush()

        return catalogueFile

    def getWorkCount(self) -> int:
        return self._workCount