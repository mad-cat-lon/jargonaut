import libcst as cst
# import jargonaut.transformations.data.primitives as primitives
# import numpy as np
import random 
# from z3 import Int, Sum, And, Solver, sat
from libcst.metadata import ParentNodeProvider, TypeInferenceProvider, PositionProvider
from libcst.metadata import ScopeProvider
from .mba_utils import rewrite_expr
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin


class ExprToLinearMBA(cst.CSTTransformer):
    """
    Converts binary operations into linear mixed boolean arithmetic expressions
    
    Attributes:
        sub_expr_depth: int range specifying recursion depth for sub-expressions, eg.
                        ((x + y) & 13) has a sub-expression (x+y)

        super_expr_depth: int range specifying recursion depth for parent expressions, eg.
                          ((x + y) & 13) has super-expression ((sub_expr) & 13)
    """

    def __init__(
        self, 
        sub_expr_depth=[1, 2], 
        super_expr_depth=[2, 20],
        inference=False
    ):
        self.inference = inference
        self.sub_expr_depth = sub_expr_depth
        self.super_expr_depth = super_expr_depth
        self.first_visit = True
        self.progress_msg = "Transforming expressions to linear MBA forms..."
        self.spinner = None
        if inference is False:
            ExprToLinearMBA.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                PositionProvider,
                ScopeProvider,
            )
        else:
            ExprToLinearMBA.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                TypeInferenceProvider,
                PositionProvider,
                ScopeProvider
            )
    
    def visit_BinaryOperation(self, node: cst.BinaryOperation):
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(Spinners.dots12, text=self.progress_msg, timer=True)
            self.spinner.start()
            self.first_visit = False
        return True

    def leave_BinaryOperation(
        self,
        original_node: cst.BinaryOperation,
        updated_node: cst.BinaryOperation
    ):  
        if self.inference is True:
            # TODO: Should use a matcher here instead of isinstance() spamming
            # We need to account for string literal concatenation 
            # "abc" + "def" counts as a BinaryOperation 
            # https://lwn.net/Articles/551426/
            if (
                isinstance(original_node.left, cst.SimpleString)
                or isinstance(original_node.right, cst.SimpleString)
            ):
                return updated_node
            left_inferred_type = ""
            right_inferred_type = ""
            # Handle KeyErrors from pyre
            try:
                left_inferred_type = self.get_metadata(
                    TypeInferenceProvider,
                    original_node.left
                )
            except KeyError:
                pass
            try:
                right_inferred_type = self.get_metadata(
                    TypeInferenceProvider,
                    original_node.right
                )
            except KeyError:
                pass
            # Account for the case where we have the following:
            # a = "abcd"
            # b = "efgh"
            # a + b
            if ("str" in left_inferred_type) or ("str" in right_inferred_type):
                return original_node
            # TODO: Account for the case where we have the following:
            # a = "abcd"
            # b = "efgh"
            # a[0] + b[1]
            # We also want to be able to transform the following:
            # a = [1, 2, 3, 4]
            # b = [4, 3, 5, 1]
            # a[0] + b[1]
            # Unfortunately, there doesn't seem to be a way to cleanly separate these
            # cases due to how Python lists and pyre work AFAIK.
            # I'd have to get the List() corresponding to the value of the subscript,
            # the value of the Index() then check the type of the Element() in the list
            if (
                isinstance(original_node.left, cst.Subscript)
                or isinstance(original_node.left, cst.Subscript)
            ):
                return updated_node
        parent_node = self.get_metadata(ParentNodeProvider, original_node)
        if isinstance(parent_node, cst.BinaryOperation):
            mba_expr = rewrite_expr(
                updated_node,
                depth=random.randint(*self.sub_expr_depth)
            )
            return mba_expr
        else:
            mba_expr = rewrite_expr(
                updated_node,
                depth=random.randint(*self.super_expr_depth)
            )
            return mba_expr

    

