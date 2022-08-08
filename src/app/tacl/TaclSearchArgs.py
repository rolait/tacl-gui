from typing import List


class TaclSearchArgs:  # pragma: no cover
    """
    Contains the arguments in the format as required by TACL for the 'search' command.
    """

    def __init__(
        self,
        catalogue: str,
        corpus: str,
        db: str,
        ngrams: List[str],

        memory: bool = False,
        ram: int = 3,
        tokenizer: str = "cbeta",
        verbose: int = 1
    ):
        self.catalogue = catalogue
        self.corpus = corpus
        self.db = db
        self.ngrams = ngrams

        self.memory = memory
        self.ram = ram
        self.tokenizer = tokenizer
        self.verbose = verbose
