# constants.py
from enum import Enum
from typing import Dict


class Mode(Enum):
    REGULAR_SPACES = 0
    NON_BREAKING_SPACES = 1


end_of_line_symbol = '\n'
space_symbols = (" ", "\u00A0")

cypher_maps:Dict[Mode, Dict[int, str]] = dict([(Mode.REGULAR_SPACES,        dict([(1, " "), (0, "  ")])),
                                               (Mode.NON_BREAKING_SPACES,   dict([(1, " "), (0, "\u00A0")]))])

decypher_maps:Dict[Mode, Dict[str, int]] = dict([(Mode.REGULAR_SPACES,      dict([(" ", 1), ("  ", 0)])),
                                               (Mode.NON_BREAKING_SPACES,   dict([(" ", 1), ("\u00A0", 0)]))])
