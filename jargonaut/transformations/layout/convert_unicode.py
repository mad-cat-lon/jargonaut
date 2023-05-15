import libcst as cst
from collections import defaultdict
import unicodedata
from functools import lru_cache


class ConvertUnicode(cst.CSTTransformer):
    def __init__(self, avoid=[]):
        self.avoid = avoid
        self.names = defaultdict(lambda: None)
        self.imports = defaultdict(lambda: None)

    @lru_cache
    def _get_codepoints(self, c):
        codepoints = [
            chr(i) for i in range(0x10FFFF)
            # Don't include anything in Enclosed Alphanumeric Supplement 
            if unicodedata.normalize("NFKC", chr(i)) == c
            and not (0x2460 <= i <= 0x24FF)
            and not (0x1F130 <= i <= 0x1F149)
        ]
        if len(codepoints) == 0:
            return c
        else:
            return codepoints

    # TODO: implement this using libcst