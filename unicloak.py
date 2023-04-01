import random
import ast
from typing import Any
import unicodedata
from functools import lru_cache
import sys


class Unicloak(ast.NodeTransformer):
    """
    Uses PEP-672 "Normalizing identifiers" to convert
    all identifiers into randomly generated Unicode equivalents
    https://blog.phylum.io/malicious-actors-use-unicode-support-in-python-to-evade-detection
    https://peps.python.org/pep-0672/#normalizing-identifiers
    """
    def __init__(self):
        self.builtins = [
            name for name, func in sorted(vars(__builtins__).items())
        ] + ["__builtins__"]
    
    @lru_cache
    def get_codepoints(self, c):
        """Gets all valid unicode codepoints given a char c"""
        # Don't include anything in Enclosed Alphanumeric Supplement 
        codepoints = [
            chr(i) for i in range(0x10FFFF)
            if unicodedata.normalize("NFKC", chr(i)) == c
            and not (0x2460 <= i <= 0x24FF)
            and not (0x1F130 <= i <= 0x1F149)
        ]
        if len(codepoints) == 0:
            return c
        else:
            return codepoints

    def cloak_id(self, identifier):
        all_codepoints = [self.get_codepoints(j) for j in identifier]
        return "".join([random.choice(i) for i in all_codepoints])
    
    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        node.name = self.cloak_id(node.name)
        return self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        if node.name[0] != "_":
            node.name = self.cloak_id(node.name)
        return self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        # TODO: improve later
        if isinstance(node.func, ast.Name):
            if node.func.id not in self.builtins:
                node.func.id = self.cloak_id(node.func.id)
            return self.generic_visit(node)
        else:
            return self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id not in self.builtins:
            node.id = self.cloak_id(node.id)
        return self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            alias.asname = self.cloak_id(alias.name)
        return self.generic_visit(node)


def main():
    if len(sys.argv) != 3:
        print("[!] unicloak.py input_file.py output_file.py")
        exit()
    else:
        with open(sys.argv[1], "r", encoding="utf-8") as in_file:
            uc = Unicloak()
            tree = ast.parse(in_file.read())
            uc.visit(tree)
            obfus = ast.unparse(tree)
            with open(sys.argv[2], "w", encoding="utf-8") as out_file:
                out_file.write(obfus)


if __name__ == "__main__":
    main()
