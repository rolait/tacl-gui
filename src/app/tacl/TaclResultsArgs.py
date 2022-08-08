
class TaclResultsArgs:  # pragma: no cover
    """
    Contains the arguments in the format as required by TACL for the 'results' command.
    """

    def __init__(
        self,
        results: str,
        tokenizer: str,
        add_label_count: bool = False,
        add_label_work_count: bool = False,
        bifurcated_extend: str = None,
        bifurcated_extend_size: int = None,
        collapse_witnesses: bool = False,
        denormalise_mapping: str = None,
        denormalised_corpus: str = None,
        excise: str = None,
        extend: str = None,
        group_by_ngram: str = None,
        group_by_witness: bool = False,
        label: str = None,
        max_count: int = None,
        max_count_work: int = None,
        max_size: int = None,
        max_works: int = None,
        min_count: int = None,
        min_count_work: int = None,
        min_size: int = None,
        min_works: int = None,
        ngrams: str = None,
        reciprocal: bool = False,
        reduce: bool = False,
        relabel: str = None,
        remove: str = None,
        sort: bool = False,
        verbose: int = 1,
        zero_fill: str = None,
    ):
        self.add_label_count = add_label_count
        self.add_label_work_count = add_label_work_count
        self.bifurcated_extend = bifurcated_extend
        self.bifurcated_extend_size = bifurcated_extend_size
        self.collapse_witnesses = collapse_witnesses
        self.denormalise_mapping = denormalise_mapping
        self.denormalised_corpus = denormalised_corpus
        self.excise = excise
        self.extend = extend
        self.group_by_ngram = group_by_ngram
        self.group_by_witness = group_by_witness
        self.label = label
        self.max_count = max_count
        self.max_count_work = max_count_work
        self.max_size = max_size
        self.max_works = max_works
        self.min_count = min_count
        self.min_count_work = min_count_work
        self.min_size = min_size
        self.min_works = min_works
        self.ngrams = ngrams
        self.reciprocal = reciprocal
        self.reduce = reduce
        self.relabel = relabel
        self.remove = remove
        self.results = results
        self.sort = sort
        self.tokenizer = tokenizer
        self.verbose = verbose
        self.zero_fill = zero_fill
