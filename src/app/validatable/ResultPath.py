import pandas
from pandas import DataFrame

from app.utils import tr

from app.validatable.ExistingFilePath import ExistingFilePath


class ResultPath(ExistingFilePath):

    def __init__(self, pathString: str):
        super().__init__(pathString, tr("result path"), False)

    def toDataFrame(self) -> DataFrame:
        return pandas\
            .read_csv(str(self), encoding='utf-8', na_filter=False)\
            .dropna(how='all')
