import ast
from typing import Any
from collections import defaultdict
import random 


class RandomizeNames(ast.NodeTransformer):
    """
    Randomizes names of imports, variables, functions, and args
    """
    def __init__(self, avoid=[], keys=["I", "i", "l"]):
        self.avoid = avoid
        self.keys = keys
        self.names = defaultdict(lambda: None)
        self.imports = defaultdict(lambda: None)
        self.msg = "Randomizing names..."

    def randomize(self):
        return ''.join([random.choice(self.keys) for _ in range(12)])
    
    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            new_asname = self.randomize()
            self.imports[alias.name] = new_asname
            alias.asname = new_asname
        return self.generic_visit(node)
        
    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            new_asname = self.randomize()
            self.imports[alias.name] = new_asname
            alias.asname = new_asname 
        return self.generic_visit(node)
    
    def visit_Name(self, node: ast.Name):
        if node.id in self.avoid or (node.id[:2] == "__" and node.id[-2:] == "__"):
            # Don't randomize
            return node
        elif self.imports[node.id] is not None:
            node.id = self.imports[node.id]
        else:
            if self.names[node.id] is None:
                self.names[node.id] = self.randomize()
            node.id = self.names[node.id]
        # No need to recurse any further
        return node
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        if node.name not in self.avoid:
            if self.names[node.name] is None:
                self.names[node.name] = self.randomize()
            node.name = self.names[node.name]
        return self.generic_visit(node)
    
    def visit_arguments(self, node: ast.arguments) -> Any:
        for arg in node.args:
            if self.names[arg.arg] is None:
                self.names[arg.arg] = self.randomize()
            arg.arg = self.names[arg.arg]
        return self.generic_visit(node)