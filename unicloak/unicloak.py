import ast
from typing import Any
from unicloak.utils.mba import mba
from unicloak.utils.unicode import unicode
from unicloak.utils.strings import binary
import random
import json 


class Unicloak(ast.NodeTransformer):
    """
    Unicloak base class that transforms nodes
    """
    def __init__(self, builtins, config_path=None):
        self.builtins = [
            name for name, func in sorted(vars(builtins).items())
        ] + ["__builtins__"]
        if config_path is None:
            f = open("default.json")
            self.config = json.load(f)

    def generic_visit(self, node: ast.AST) -> ast.AST:
        return super().generic_visit(node)    
    
    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        node.name = unicode.convert_unicode(node.name)
        return self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        if node.name[0] != "_":
            node.name = unicode.convert_unicode(node.name)
        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id not in self.builtins:
            node.id = unicode.convert_unicode(node.id)
        return self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            alias.name = unicode.convert_unicode(alias.name)
        return node
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        node.module = unicode.convert_unicode(node.module)
        for alias in node.names:
            alias.name = unicode.convert_unicode(alias.name)
        return node

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
            return node
        return self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> Any:
        if isinstance(node.value, int):
            obfus = mba.generate_linear_mba(node)
            node.value = obfus
            return obfus
        if isinstance(node.value, str):
            # Placeholders for now
            keys = ["Ꭓ", "𝑿", "𝙓", "𝚇"]
            obfus = binary(random.sample(keys, 2), node.value)
            return obfus.value
        return node
