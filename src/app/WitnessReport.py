from typing import List

from app.Witness import Witness
from app.utils import tr


class WitnessReport:
    """
    Report containing missing/changed/new witnesses.
    """
    _missingWitnesses: List[Witness]

    _changedWitnesses: List[Witness]

    _newWitnesses: List[Witness]

    def __init__(self):
        self._missingWitnesses = []
        self._changedWitnesses = []
        self._newWitnesses = []

    def addMissingWitness(self, witness: Witness):
        self._missingWitnesses.append(witness)

    def addChangedWitness(self, witness: Witness):
        self._changedWitnesses.append(witness)

    def addNewWitnesses(self, witness: Witness):
        self._newWitnesses.append(witness)

    def hasMissingWitnesses(self) -> bool:
        return len(self._missingWitnesses) != 0

    def hasChangedOrAddedWitnesses(self) -> bool:
        return len(self._changedWitnesses) != 0 or len(self._newWitnesses) != 0

    def createReportText(self) -> str:
        reports: List[str] = []

        self._createReportFromList(reports, self._missingWitnesses, tr("Missing Witnesses"))
        self._createReportFromList(reports, self._changedWitnesses, tr("Changed Witnesses"))
        self._createReportFromList(reports, self._newWitnesses, tr("New Witnesses"))

        return '\n\n'.join(reports)

    def _createReportFromList(self, reports: List[str], witnessList: list[Witness], title: str) -> None:
        if len(witnessList) == 0:
            return

        reports.append("=== {} ({})===\n{}".format(
            title,
            len(witnessList),
            '\n'.join(map(str, witnessList))
        ))


