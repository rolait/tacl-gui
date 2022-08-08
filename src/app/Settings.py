from typing import Optional

from app.validatable.Id import Id


class Settings:

    def __init__(
        self,
        lastSelectedDatabaseId: Optional[Id],
        lastOpenPath: str,
        lastSavePath: str
    ):
        self._lastSelectedDatabaseId = lastSelectedDatabaseId
        self._lastSavePath = lastSavePath
        self._lastOpenPath = lastOpenPath

    def getLastSelectedDatabaseId(self) -> Optional[Id]:
        return self._lastSelectedDatabaseId

    def setLastSelectedDatabaseId(self, id: Optional[Id]) -> None:
        self._lastSelectedDatabaseId = id

    def getLastSavePath(self) -> str:
        return self._lastSavePath

    def setLastSavePath(self, lastSavePath: str) -> None:
        self._lastSavePath = lastSavePath

    def getLastOpenPath(self) -> str:
        return self._lastOpenPath

    def setLastOpenPath(self, lastOpenPath: str) -> None:
        self._lastOpenPath = lastOpenPath

