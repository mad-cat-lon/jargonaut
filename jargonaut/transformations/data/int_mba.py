import libcst as cst
import random 
from libcst.metadata import ParentNodeProvider, TypeInferenceProvider, PositionProvider
from libcst.metadata import ScopeProvider
from libcst.metadata import FunctionScope, GlobalScope
from .mba_utils import constant_to_mba
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin


class ConstIntToLinearMBA(cst.CSTTransformer):
    """
    Transforms constants to MBA expressions
    Can specify whether you want to use affine or polynomial functions (todo)
    
    Attributes:
        n_term_range: range for the number of terms in the MBA expression
        inference:  Use type inference
    """

    def __init__(self, n_terms_range=[4, 6], probability=0.7, inference=False):
        self.n_terms_range = n_terms_range
        self.probability = probability
        self.inference = inference
        self.first_visit = True
        self.progress_msg = "Transforming all integer constants to linear MBA forms..."
        self.spinner = None
        if inference is False:
            ConstIntToLinearMBA.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                PositionProvider,
                ScopeProvider,
            )
        else:
            ConstIntToLinearMBA.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                TypeInferenceProvider,
                PositionProvider,
                ScopeProvider
            )
        self.func_ints = []
        self.global_ints = []
    
    def get_global_ints_for_node(self, node):
        """
        Filters self.global_ints for int names that appear
        before current node in code 
        """
        node_pos = (self.get_metadata(PositionProvider, node).start).line
        valid_global_ints = [
            name[0] for name in self.global_ints
            if name[1] < node_pos
        ]
        return valid_global_ints

    def insert_random_vals(self, constant_mba):
        x_val = random.randint(0, 1000)
        y_val = random.randint(0, 1000)
        constant_mba = constant_mba.replace("x", str(x_val))
        constant_mba = constant_mba.replace("y", str(y_val))
        return constant_mba

    def visit_Name(self, node: cst.Name):
        try:
            scope = self.get_metadata(ScopeProvider, node)
            if isinstance(scope, GlobalScope):
                try:
                    inferred_type = self.get_metadata(TypeInferenceProvider, node)
                    node_pos = self.get_metadata(PositionProvider, node)
                    if inferred_type == "int":
                        self.global_ints.append((node, (node_pos.start).line))
                except KeyError:
                    pass
        except KeyError:
            pass
        return True

    def visit_FunctionDef(self, node: cst.FunctionDef):
        """
        Collects all integer parameters by inspecting type annotations
        (works with SeedParams()), not using Pyre for now due to issues
        """
        int_params = []
        for param in node.params.params:
            if param.annotation:
                if param.annotation.annotation.value == "int":
                    int_params.append(param.name)
        self.func_ints = int_params
        return True 
    
    def leave_FunctionDef(
        self,
        original_node: cst.FunctionDef,
        updated_node: cst.FunctionDef
    ):
        self.func_ints = []
        return updated_node
    
    def visit_Integer(self, node: cst.Integer):
        if self.first_visit:
            self.spinner = kbi_safe_yaspin(Spinners.dots12, text=self.progress_msg, timer=True)
            self.spinner.start()
            self.first_visit = False

    def leave_Integer(
        self, 
        original_node: cst.Integer,
        updated_node: cst.Integer
    ):
        scope = self.get_metadata(ScopeProvider, original_node)
        constant_mba = constant_to_mba(
            int(original_node.evaluated_value),
            n_terms=random.choice(self.n_terms_range),
            as_obj=False
        )
        # HACK: Should find a way to use matchers here 
        if isinstance(scope, FunctionScope):
            if self.inference:
                if self.func_ints:
                    # print(f"[FUNC] Available names: {self.func_ints[-1]}")
                    x = random.choice(self.func_ints)
                    y = random.choice(self.func_ints)
                    constant_mba = constant_mba.replace("x", x.value)
                    constant_mba = constant_mba.replace("y", y.value)
                    return cst.parse_expression(constant_mba)
                else:
                    # print("[FUNC] No names available")
                    # Try global scope
                    valid_global_ints = self.get_global_ints_for_node(original_node)
                    if len(valid_global_ints) > 0:
                        # print("[FUNC] Trying global ints")
                        x = random.choice(valid_global_ints)
                        y = random.choice(valid_global_ints)
                        constant_mba = constant_mba.replace("x", x.value)
                        constant_mba = constant_mba.replace("y", y.value)
                        return cst.parse_expression(constant_mba)
                    else:
                        # print("[FUNC] no usable global ints found")
                        constant_mba = self.insert_random_vals(constant_mba)
                        return cst.parse_expression(constant_mba)
            else:
                constant_mba = self.insert_random_vals(constant_mba)
                return cst.parse_expression(constant_mba)
        elif isinstance(scope, GlobalScope):
            # print("In global scope")
            if self.inference:
                valid_global_ints = self.get_global_ints_for_node(original_node)
                if len(valid_global_ints) > 0:
                    # print(f"[GLOB] Available names: {self.glob_ints}")
                    x = random.choice(valid_global_ints)
                    y = random.choice(valid_global_ints)
                    constant_mba = constant_mba.replace("x", x.value)
                    constant_mba = constant_mba.replace("y", y.value)
                    return cst.parse_expression(constant_mba)
                else:
                    # print("[GLOB] No names available")
                    constant_mba = self.insert_random_vals(constant_mba)
                    return cst.parse_expression(constant_mba)
            else:
                constant_mba = self.insert_random_vals(constant_mba)
                return cst.parse_expression(constant_mba)
        else:
            constant_mba = self.insert_random_vals(constant_mba)
            return cst.parse_expression(constant_mba)