from libcst.metadata import QualifiedNameProvider, QualifiedNameSource, ScopeProvider, ClassScope
import libcst as cst
import random 
from typing import Optional


class RandomizeNames(cst.CSTTransformer):
    """
    Replaces names with a randomized string.
    Dpes not replace attributes or methods as of right now - type 
    inferencing will be done later to do this without breaking
    the obfuscated code
    """
    METADATA_DEPENDENCIES = (QualifiedNameProvider, ScopeProvider,)
    
    def rand_name(self):
        keys = ["I", "l", "i"]
        return ''.join(random.choices(keys, k=12))
    
    def __init__(self):
        self.randomize_map = dict()
        self.avoid_names = ["self", "__init__", "main", "super"]
        self.ignore = False

    def visit_Name(self, node: cst.Name) -> Optional[bool]:
        qualified_name = list(self.get_metadata(QualifiedNameProvider, node))
        # Don't replace builtins 
        # We'll worry about dealing with modules later 
        # Only replace source=<QualifiedNameSource.Local: 3>
        if node.value not in self.avoid_names:
            if len(qualified_name) != 0:
                qualified_name = qualified_name[0]
                if qualified_name.source == QualifiedNameSource.LOCAL:
                    if qualified_name.name not in self.randomize_map:
                        self.randomize_map[qualified_name.name] = self.rand_name()
                    self.ignore = False
                    return (
                        True
                    )
        self.ignore = True
        return (
            False
        )
    
    def leave_Name(
            self, 
            original_node: cst.Name,
            updated_node: cst.Name
    ) -> None:
        qualified_name = list(self.get_metadata(QualifiedNameProvider, original_node))
        if self.ignore:
            return updated_node
        else:
            qualified_name = qualified_name[0]
            scope = self.get_metadata(ScopeProvider, original_node)
            # Don't change names for class methods until we have type inferencing with mypy built in
            if not isinstance(scope, ClassScope):
                if qualified_name.name in self.randomize_map:
                    # print(f"{qualified_name}.name -> {self.randomize_map[qualified_name.name]}")
                    return updated_node.with_changes(
                        value=self.randomize_map[qualified_name.name]
                    )
        return updated_node 