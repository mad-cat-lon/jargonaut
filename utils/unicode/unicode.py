from functools import lru_cache
import random
import unicodedata


@lru_cache
def get_codepoints(c):
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


def convert_unicode(identifier):
    """
    Uses PEP-672 "Normalizing identifiers" to convert
    all identifiers into randomly generated Unicode equivalents
    https://blog.phylum.io/malicious-actors-use-unicode-support-in-python-to-evade-detection
    https://peps.python.org/pep-0672/#normalizing-identifiers
    """
    all_codepoints = [get_codepoints(j) for j in identifier]
    variant = ''.join([random.choice(i) for i in all_codepoints])
    valid = False
    # Regenerate variant if it's still invalid somehow 
    # Hacky solution, read Unicode Standard Annex #15 and re-implement later
    while valid is False:
        try:
            exec(f"{variant}=123")
            valid = True
        except SyntaxError:
            variant = ''.join([random.choice(i) for i in all_codepoints])
    return variant
