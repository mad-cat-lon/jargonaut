import ast
from collections import defaultdict
import random 
import unicodedata
from functools import lru_cache


class ConvertUnicode(ast.NodeTransformer):
    def __init__(self, avoid=[]):
        self.avoid = avoid
        self.names = defaultdict(lambda: None)
        self.imports = defaultdict(lambda: None)
        self.msg = "Converting identifiers to Unicode equivalents..."
    
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

    def unicode_variant(self, identifier):
        """
        Uses PEP-672 "Normalizing identifiers" to convert
        all identifiers into randomly generated Unicode equivalents
        https://blog.phylum.io/malicious-actors-use-unicode-support-in-python-to-evade-detection
        https://peps.python.org/pep-0672/#normalizing-identifiers
        """
        all_codepoints = [self._get_codepoints(j) for j in identifier]
        variant = ''.join([random.choice(i) for i in all_codepoints])
        valid = False
        # Regenerate variant if it's still invalid somehow 
        # Hacky solution, read Unicode Standard Annex #15 and re-implement later
        while valid is False:
            try:
                exec(f"{variant}=123")
                valid = True
            except SyntaxError or SyntaxError:
                variant = ''.join([random.choice(i) for i in all_codepoints])
        return variant

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            new_name = self.unicode_variant(alias.name)
            alias.name = new_name 
        return node
    
    def visit_ImportFrom(self, node: ast.ImportFrom):
        node.module = self.unicode_variant(node.module)
        for alias in node.names:
            new_name = self.unicode_variant(alias.name)
            alias.name = new_name 
        return node

    def visit_ClassDef(self, node: ast.ClassDef):
        node.name = self.unicode_variant(node.name)
        return self.generic_visit(node)
    