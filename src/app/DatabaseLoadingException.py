from typing import Optional


class DatabaseLoadingException(Exception):

    def __init__(self, msg: str, name: str, path: str, corpusPath: str, details: str = None):
        super().__init__(msg)

        self._name = name
        self._path = path
        self._corpusPath = corpusPath
        self._details = details

    def getName(self) -> str:
        return self._name

    def getPath(self) -> str:
        return self._path

    def getCorpusPath(self) -> str:
        return self._corpusPath

    def getDetails(self) -> Optional[str]:
        return self._details