class TaclNgramsArgs:  # pragma: no cover
    """
    Contains the arguments in the format as required by TACL for the 'ngrams' command.
    """

    def __init__(
        self,
        corpus: str,
        db: str,
        min_size: int,
        max_size: int,

        catalogue: str = None,
        memory: int = None,
        ram: int = None,
        tokenizer: str = "cbeta"
    ):

        self.corpus = corpus
        self.db = db
        self.min_size = min_size
        self.max_size = max_size

        self.catalogue = catalogue
        self.memory = memory
        self.ram = ram
        self.tokenizer = tokenizer
