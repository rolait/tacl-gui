import os
import sqlite3
from pathlib import Path
from typing import Optional, Set

from app.Witness import Witness
from app.WitnessReport import WitnessReport
from app.inputValidator.InputValidator import InputValidator
from app.inputValidator.ValidationError import ValidationError
from app.utils import tr
from app.validatable.CorpusPath import CorpusPath
from app.validatable.DatabaseNGramLengths import DatabaseNGramLengths
from app.validatable.DatabaseName import DatabaseName
from app.validatable.DatabasePath import DatabasePath
from app.validatable.Id import Id


class Database:

    def __init__(
        self,
        id: Optional[Id],
        name: DatabaseName,
        path: DatabasePath,
        corpusPath: CorpusPath,
        nGramLengths: DatabaseNGramLengths
    ):
        self._name = name
        self._path = path
        self._corpusPath = corpusPath
        self._nGramLengths = nGramLengths
        self._id = id

    def getId(self) -> Optional[Id]:
        return self._id

    def getName(self) -> DatabaseName:
        return self._name

    def setName(self, name: DatabaseName) -> None:
        self._name = name

    def getPath(self) -> DatabasePath:
        return self._path

    def getCorpusPath(self) -> CorpusPath:
        return self._corpusPath

    def setNgramLengths(self, ngramLengths: DatabaseNGramLengths) -> None:
        self._nGramLengths = ngramLengths

    def getNGramLengths(self) -> DatabaseNGramLengths:
        return self._nGramLengths

    def getNGramMinLength(self) -> int:
        return self._nGramLengths.getMinLength()

    def getNGramMaxLength(self) -> int:
        return self._nGramLengths.getMaxLength()

    def __eq__(self, other):
        return isinstance(other, Database) and other.getId() == self._id

