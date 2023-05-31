import libcst as cst
# import jargonaut.transformations.data.primitives as primitives
# import numpy as np
import random 
# from z3 import Int, Sum, And, Solver, sat
from libcst.metadata import ParentNodeProvider, TypeInferenceProvider, PositionProvider
from libcst.metadata import ScopeProvider
from .mba_utils import rewrite_expr


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
        self.progress_msg = "[-] Transforming expressions to linear MBA forms..."
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
    
    def leave_BinaryOperation(
        self,
        original_node: cst.BinaryOperation,
        updated_node: cst.BinaryOperation
    ):        
        if self.first_visit is True:
            print(self.progress_msg)
            self.first_visit = False
        if self.inference is True:
            # We need to account for string literal concatenation 
            # "abc" + "def" counts as a BinaryOperatiojn
            # https://lwn.net/Articles/551426/
            if (
                isinstance(original_node.left, cst.SimpleString)
                or isinstance(original_node.right, cst.SimpleString)
            ):
                return original_node
            # Account for the case where we have the following:
            # a = "abcd"
            # b = "efgh"
            # a + b
            if original_node.left and original_node.right:
                left_inferred_type = None
                right_inferred_type = None
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
                if left_inferred_type and right_inferred_type:
                    if (
                        left_inferred_type == "str"
                        or right_inferred_type == "str"
                    ):
                        return original_node
                    return original_node
                return original_node
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

    

