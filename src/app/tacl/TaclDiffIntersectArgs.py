class TaclDiffIntersectArgs:  # pragma: no cover
    """
    Contains the arguments in the format as required by TACL for the 'diff' and 'intersect' commands.
    """

    def __init__(
        self,
        catalogue: str,
        corpus: str,
        database: str,
        asymmetric: str = None,
        memory: bool = False,
        ram: int = 3,
        tokenizer: str = "cbeta",
        verbose: int = 1
    ):
        self.asymmetric = asymmetric
        self.catalogue = catalogue
        self.corpus = corpus
        self.db = database
        self.memory = memory
        self.ram = ram
        self.tokenizer = tokenizer
        self.verbose = verbose
