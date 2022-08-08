from enum import Enum


class ResultType(Enum):
    DIFFERENCE = "difference"
    INTERSECT = "intersect"
    SEARCH = "search"
    SUPPLIED_INTERSECT = "supplied intersect"
    FILTER_RATIONALISE = "filter rationalise"
