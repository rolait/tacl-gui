from app.utils import tr
from app.validatable.ExistingFilePath import ExistingFilePath


class DatabasePath(ExistingFilePath):

    def __init__(self, pathString: str):
        super().__init__(pathString, tr("database path"), False)