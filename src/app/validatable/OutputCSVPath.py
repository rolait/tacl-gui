from app.utils import tr

from app.validatable.ResultPath import ResultPath
from app.validatable.WritableFilePath import WritableFilePath


class OutputCSVPath(WritableFilePath):

    def __init__(self, pathString: str):
        if not pathString.lower().endswith(".csv"):
            pathString = pathString + ".csv"

        super().__init__(pathString, tr("output csv file"))

    def toResultPath(self) -> ResultPath:
        return ResultPath(str(self._path))
