import ast
from typing import Any
from unicloak.utils.mba import mba
from unicloak.utils.unicode import unicode
from unicloak.utils.strings import binary, obfus_name
from collections import defaultdict
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
        # Associate names with obfuscated names to avoid recomputing  
        self.names = defaultdict(lambda: None)
        # Store imports so we don't accidentally obfuscate them
        self.imports = defaultdict(lambda: None)
        if config_path is None:
            f = open("default.json")
            self.config = json.load(f)

    def generic_visit(self, node: ast.AST) -> ast.AST:
        return super().generic_visit(node)    
    
    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        node.name = unicode.convert_unicode(node.name)
        return self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        if node.name in self.builtins:
            node.name = unicode.convert_unicode(node.name)
        else:
            if self.names[node.name] is None:
                self.names[node.name] = obfus_name()
            #print(f"Renaming {node.name} to {self.names[node.name]}")
            node.name = self.names[node.name]
            for arg in node.args.args:
                if self.names[arg.arg] is None:
                    self.names[arg.arg] = obfus_name()
                arg.arg = self.names[arg.arg]
            return self.generic_visit(node)
            
    def visit_Lambda(self, node: ast.Lambda) -> Any:
        for arg in node.args.args:
            if isinstance(arg, ast.Name):
                if self.names[arg.arg] is None:
                    self.names[arg.arg] = obfus_name()
                arg.arg = self.names[arg.arg]
        return self.generic_visit(node)
    
    def visit_Name(self, node: ast.Name) -> Any:
        if node.id in self.builtins:
            #print(f"Name({node.id}) in builtins. Generating Unicode variant")
            node.id = unicode.convert_unicode(node.id)
        elif self.imports[node.id] is not None:
            #print(f"Name({node.id}) in imports. Name({node.id}) -> Name({self.imports[node.id]})")
            node.id = self.imports[node.id]
        else:
            if self.names[node.id] is None:
                self.names[node.id] = obfus_name()
            #print(f"Name({node.id})->Name({self.names[node.id]})")
            node.id = self.names[node.id]
        return self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            new_name = unicode.convert_unicode(alias.name)
            new_asname = obfus_name()
            self.imports[alias.name] = new_asname
            alias.name = new_name 
            alias.asname = new_asname
        return node
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        node.module = unicode.convert_unicode(node.module)
        for alias in node.names:
            new_name = unicode.convert_unicode(alias.name)
            new_asname = obfus_name()
            self.imports[alias.name] = new_asname
            alias.name = new_name 
            alias.asname = new_asname
        return node

    def visit_Expr(self, node: ast.Expr) -> Any:
        # Obfuscate expressions with BinOps using MBA
        if isinstance(node.value, ast.BinOp):
            obfus = mba.generate_linear_mba(node.value)
            node.value = obfus
        return self.generic_visit(node)
        
    def visit_Assign(self, node: ast.Assign) -> Any:
        # Obfuscate assignments with BinOps using MBA
        if isinstance(node.value, ast.BinOp):
            obfus = mba.generate_linear_mba(node.value)
            node.value = obfus
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
