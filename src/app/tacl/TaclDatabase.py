import os
import sqlite3
from pathlib import Path
from sqlite3 import Connection
from typing import Optional, Set

from app.DatabaseLoadingException import DatabaseLoadingException
from app.Witness import Witness
from app.WitnessReport import WitnessReport
from app.validatable.CorpusPath import CorpusPath
from app.validatable.DatabaseNGramLengths import DatabaseNGramLengths
from app.validatable.DatabasePath import DatabasePath
from app.inputValidator.ValidationError import ValidationError


class TaclDatabase:

    def __init__(self, databasePath: DatabasePath):
        self._path = databasePath

    def extractNgramLengths(self) -> Optional[DatabaseNGramLengths]:
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("select min(size) as minLength, max(size) as maxLength from TextHasNGram")
        row = cursor.fetchone()
        minLength = row["minLength"];
        maxLength = row["maxLength"];

        if not isinstance(minLength, int) or not isinstance(maxLength, int):
            raise ValidationError()

        return DatabaseNGramLengths(minLength, maxLength)

    def createWitnessReport(self, corpusPath: CorpusPath):
        report = WitnessReport()
        witnessSet: Set[str] = set()

        self._checkForMissingAndChangedWitnesses(corpusPath, witnessSet, report)
        self._checkForNewWitnesses(corpusPath, witnessSet, report)

        return report

    def _checkForMissingAndChangedWitnesses(self, corpusPath: CorpusPath, witnessSet: Set[str], report: WitnessReport):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT work, siglum, checksum FROM Text ORDER BY work, siglum")

            for row in cursor:
                witness = Witness(corpusPath, row["work"], row["siglum"])
                witnessSet.add(str(witness))

                if not witness.exists():
                    report.addMissingWitness(witness)
                    continue

                if row["checksum"] != witness.calculateChecksum():
                    report.addChangedWitness(witness)

            cursor.close()
            connection.close()
        except sqlite3.Error as error:
            raise DatabaseLoadingException(
                str(error),
                os.path.basename(str(self._path)),
                self._path,
                corpusPath
            )

    def _checkForNewWitnesses(self, corpusPath: CorpusPath,  witnessSet: Set[str], report: WitnessReport):
        corpusDir = os.listdir(str(corpusPath))
        corpusDir.sort()

        for workDirName in corpusDir:
            workPath = Path(str(corpusPath), workDirName)

            if not workPath.is_dir():
                continue

            workDir = os.listdir(workPath)
            workDir.sort()

            for witnessName in workDir:
                witnessPath = Path(workPath, witnessName).absolute()

                if not witnessPath.is_file():
                    continue

                witness = Witness(corpusPath, workDirName, witnessPath.stem)

                if not str(witness) in witnessSet:
                    report.addNewWitnesses(witness)

    def connect(self) -> Connection:
        connection = sqlite3.connect(str(self._path))
        connection.row_factory = sqlite3.Row

        return connection
