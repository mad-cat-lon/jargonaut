from libcst.metadata import QualifiedNameProvider, QualifiedNameSource, ScopeProvider, ClassScope
# from libcst.metadata import TypeInferenceProvider
import libcst as cst
import random 
from typing import Optional
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin


class RandomizeNames(cst.CSTTransformer):
    """
    Replaces names with a randomized string.
    Dpes not replace attributes or methods as of right now - type 
    inferencing will be done later to do this without breaking
    the obfuscated code
    """

    METADATA_DEPENDENCIES = (
        QualifiedNameProvider, 
        ScopeProvider
    )
    
    def __init__(self):
        self.randomize_map = dict()
        self.avoid_names = ["self", "__init__", "main", "super"]
        self.ignore = False
        self.first_visit = True
        self.progress_msg = "Randomizing variable names..."
        self.spinner = None

    def rand_name(self):
        keys = [
            "I",
            "l",
            "i",
            "Î",
            "Ĳ",
            "ĳ",
            "ǉ",
            "Ḭ",
            "j",
            "J",
            "Ĵ",
            "ⅉ",
            "ｊ"
        ]
        return ''.join(random.choices(keys, k=30))
    
    def visit_Name(self, node: cst.Name) -> Optional[bool]:
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(
                Spinners.simpleDotsScrolling,
                text=self.progress_msg,
                timer=True
            )
            self.spinner.start()
            self.first_visit = False
        qualified_names = list(self.get_metadata(QualifiedNameProvider, node))
        # Don't replace builtins 
        # We'll worry about dealing with modules later 
        # Only replace source=<QualifiedNameSource.Local: 3>
        if node.value not in self.avoid_names:
            if len(qualified_names) == 1:
                qualified_name = qualified_names[0]
                if qualified_name.source == QualifiedNameSource.LOCAL:
                    if qualified_name.name not in self.randomize_map:
                        self.randomize_map[qualified_name.name] = self.rand_name()
                    self.ignore = False
                    return True
        self.ignore = True
        return False
    
    def leave_Name(
        self, 
        original_node: cst.Name,
        updated_node: cst.Name
    ) -> cst.Name:
        if self.ignore:
            return updated_node
        else:
            scope = self.get_metadata(ScopeProvider, original_node)
            qualified_names = list(scope.get_qualified_names_for(original_node))
            qualified_name = qualified_names[0]
            # Don't change names for class methods or attributes yet
            if (
                not isinstance(scope, ClassScope)
                and qualified_name.source == QualifiedNameSource.LOCAL
            ):
                if qualified_name.name in self.randomize_map:
                    # print(f"{qualified_name}.name -> {self.randomize_map[qualified_name.name]}")
                    return updated_node.with_changes(
                        value=self.randomize_map[qualified_name.name]
                    )
        return updated_node