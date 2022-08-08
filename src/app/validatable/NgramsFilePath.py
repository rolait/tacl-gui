from app.utils import tr

from app.validatable.ExistingFilePath import ExistingFilePath


class NgramsFilePath(ExistingFilePath):

    def __init__(self, pathString: str):
        super().__init__(pathString, tr("n-grams file"), False)