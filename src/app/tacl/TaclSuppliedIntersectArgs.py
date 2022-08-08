from typing import List


class TaclSuppliedIntersectArgs:  # pragma: no cover
    """
    Object which holds attributes as required by the sintersect function of TACL.
    """

    def __init__(
        self,
        db: str,
        labels: List[str],
        supplied: List[str],
        memory: bool = False,
        ram: int = 3,
        verbose: int = 1
    ):
        self.db = db
        self.labels = labels
        self.supplied = supplied
        self.memory = memory
        self.ram = ram
        self.verbose = verbose
