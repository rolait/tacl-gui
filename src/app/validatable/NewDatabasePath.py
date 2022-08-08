from app.utils import tr

from app.validatable.DatabasePath import DatabasePath
from app.validatable.WritableFilePath import WritableFilePath


class NewDatabasePath(WritableFilePath):

    def __init__(self, pathString: str):
        super().__init__(pathString, tr("database path"))

    def toExistingDatabasePath(self) -> DatabasePath:
        return DatabasePath(str(self._path))