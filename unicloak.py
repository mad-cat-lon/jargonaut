import random
import ast
from typing import Any
import unicodedata
from functools import lru_cache
import sys
from utils.mba import mba
from utils.unicode import unicode

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
    
    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        node.name = self.cloak_id(node.name)
        return self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        if node.name[0] != "_":
            node.name = self.cloak_id(node.name)
        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id not in self.builtins:
            node.id = self.cloak_id(node.id)
        return self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            alias.name = unicode.convert_unicode(alias.name)
        return self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr) -> Any:
        # Obfuscate expressions with BinOps using MBA
        if isinstance(node.value, ast.BinOp):
            obfus = mba.generate_linear_mba(node.value)
            node.value = obfus
            return node
        return self.generic_visit(node)
        
    def visit_Assign(self, node: ast.Assign) -> Any:
        # Obfuscate assignments with BinOps using MBA
        if isinstance(node.value, ast.BinOp):
            obfus = mba.generate_linear_mba(node.value)
            node.value = obfus
            return self.generic_visit(node)
        return self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> Any:
        if isinstance(node.value, int):
            obfus = mba.generate_linear_mba(node)
            node.value = obfus.value
            return obfus.value
        elif isinstance(node.value, str):
            pass
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
