import libcst as cst
import random 
from libcst.metadata import ParentNodeProvider, TypeInferenceProvider, PositionProvider
from libcst.metadata import ScopeProvider
from libcst.metadata import GlobalScope
from .mba_utils import constant_to_linear_mba
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin
from typing import Tuple, List


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
        if inference:
            ConstIntToLinearMBA.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                TypeInferenceProvider,
                PositionProvider,
                ScopeProvider
            )
        else:
            ConstIntToLinearMBA.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                PositionProvider,
                ScopeProvider,
            )
        self.func_ints = []
        self.global_ints = []
    
    def get_global_ints_for_node_pos(self, node_pos):
        """
        Filters self.global_ints for int names that appear
        before current node in code 
        """
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

    def replace_and_parse(self, mba_expr: str, x_val: str, y_val: str) -> cst.BaseExpression:
        mba_expr = mba_expr.replace("x", x_val).replace("y", y_val)
        return cst.parse_expression(mba_expr)

    def get_replacements_from_scope(self, ints: List[int]) -> Tuple[str, str]:
        """Helper to get replacements from given scope."""
        x = random.choice(ints)
        y = random.choice(ints)
        return x.value, y.value

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
                    int_params.append(param.name.value)
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
        constant_mba = constant_to_linear_mba(
            int(original_node.evaluated_value),
            n_terms=random.choice(self.n_terms_range),
            as_obj=False
        )

        if self.inference:
            scope = self.get_metadata(ScopeProvider, original_node)
            # print("="*50)
            available = self.func_ints
            # print(available)
            try:
                node_pos = self.get_metadata(PositionProvider, original_node)
                available = available + [
                    i.value for i in self.get_global_ints_for_node_pos(node_pos.start.line)
                ]
                for assign in scope.assignments:
                    assign_node = assign.node
                    try:
                        inferred_type = self.get_metadata(TypeInferenceProvider, assign_node)
                        assign_pos = self.get_metadata(PositionProvider, assign_node)
                        # Add a margin of safety to prevent default params using other seed parameters
                        if node_pos.start.line > assign_pos.start.line+5 and inferred_type == "int":
                            available.append(assign_node.value)
                    except KeyError:
                        pass
            except KeyError:
                pass
            if available:
                # print(available)
                # print("="*50)
                x_val = random.choice(available)
                y_val = random.choice(available)
                return self.replace_and_parse(constant_mba, x_val, y_val)
            else:
                constant_mba = self.insert_random_vals(constant_mba)
                return cst.parse_expression(constant_mba)
            """
            valid_ints = []
            if isinstance(scope, FunctionScope) and self.func_ints:
                valid_ints = self.func_ints
            elif (
                isinstance(scope, GlobalScope) 
                or (isinstance(scope, FunctionScope) and not self.func_ints)
            ):
                valid_ints = self.get_global_ints_for_node(original_node)
            if valid_ints:
                x_val, y_val = self.get_replacements_from_scope(valid_ints)
                return self.replace_and_parse(constant_mba, x_val, y_val)
            """
        # Either not in inference mode or no valid integers found in scope
        constant_mba = self.insert_random_vals(constant_mba)
        return cst.parse_expression(constant_mba)