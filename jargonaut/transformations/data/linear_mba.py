import libcst as cst
# import jargonaut.transformations.data.primitives as primitives
# import numpy as np
import random 
# from z3 import Int, Sum, And, Solver, sat
import platform
from libcst.metadata import ParentNodeProvider, TypeInferenceProvider, PositionProvider
import os
script_dir = os.path.dirname(__file__) 


def get_data(operator: cst.BaseBinaryOp, depth):
    system = platform.system()
    if system == "Windows":
        data_path = "mba_data\\"
    elif system == "Darwin" or system == "Linux":
        data_path = "mba_data/"
    if isinstance(operator, cst.Add):
        data_path += f"add_depth{depth}.txt"
    elif isinstance(operator, cst.Subtract):
        data_path += f"sub_depth{depth}.txt"
    elif isinstance(operator, cst.BitAnd):
        data_path += f"and_depth{depth}.txt"
    elif isinstance(operator, cst.BitOr):
        data_path += f"or_depth{depth}.txt"
    elif isinstance(operator, cst.BitXor):
        data_path += f"xor_depth{depth}.txt"
    else: 
        return False
    abs_path = os.path.join(script_dir, data_path)
    with open(abs_path) as f:
        data = [line.replace("\n", "") for line in f.readlines()]
        return data


def rewrite_expr(node: cst.BinaryOperation, depth=2):
    operator = node.operator
    expr_dataset = get_data(operator, depth)
    if expr_dataset is False:
        return node
    mba_expr = random.choice(expr_dataset)
    # print("="*80)
    # print(f"mba_expr: {mba_expr} -> {cst.parse_module('').code_for_node(node)}")
    left_as_code = "(" + cst.parse_module("").code_for_node(node.left) + ")"
    right_as_code = "(" + cst.parse_module("").code_for_node(node.right) + ")"
    # Prevent clashes in case we use the same var as the expression
    x_name = ''.join(random.choices("abcdef", k=10))
    y_name = ''.join(random.choices("abcdef", k=10))
    mba_expr = mba_expr.replace("x", x_name)
    mba_expr = mba_expr.replace("y", y_name)
    mba_expr = mba_expr.replace(x_name, left_as_code)
    # print(f"mba-expr sub left: {mba_expr}")
    mba_expr = mba_expr.replace(y_name, right_as_code)
    # print(f"mba-expr sub right: {mba_expr}")
    mba_expr = cst.parse_expression(mba_expr)
    # print(f"final: {cst.parse_module('').code_for_node(mba_expr)}")
    # print("="*80)
    return mba_expr


class LinearMBA(cst.CSTTransformer):
    """
    Converts constants and binary operations into linear mixed boolean arithmetic expressions
    """
    METADATA_DEPENDENCIES = (
        ParentNodeProvider,
        TypeInferenceProvider,
        PositionProvider,
    )
    
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
        self.progress_msg = "[-] Obfuscating expressions with linear MBA expressions..."
        if inference is False:
            LinearMBA.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                PositionProvider,
            )
        else:
            LinearMBA.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                TypeInferenceProvider,
                PositionProvider,
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
                        isinstance(left_inferred_type, cst.SimpleString)
                        or isinstance(right_inferred_type, cst.SimpleString)
                    ):
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


"""
NUM_TERMS = 6 

truth_table = np.array([
    [0, 0, 0, 1],  # x & y
    [0, 0, 1, 0],  # x & ~y
    [0, 0, 1, 1],  # x
    [0, 1, 0, 0],  # ~x & y
    [0, 1, 0, 1],  # y
    [0, 1, 1, 0],  # x ^ y
    [0, 1, 1, 1],  # x | y
    [1, 0, 0, 0],  # ~(x | y)
    [1, 0, 0, 1],  # ~(x ^ y)
    [1, 0, 1, 0],  # ~y
    [1, 0, 1, 1],  # x | ~y
    [1, 1, 0, 0],  # ~x
    [1, 1, 0, 1],  # ~x | y
    [1, 1, 1, 0],  # ~(x & y)
    [1, 1, 1, 1],  # -1
])


func_list = [
    primitives.x_and_y,
    primitives.x_and_not_y,
    primitives.x,
    primitives.not_x_and_y,
    primitives.y,
    primitives.x_xor_y,
    primitives.x_or_y,
    primitives.not_inc_x_or_y,
    primitives.not_inc_x_xor_y,
    primitives.not_y,
    primitives.x_or_not_y,
    primitives.not_x,
    primitives.not_x_or_y,
    primitives.not_inc_x_and_y,
    primitives.min_one
]


def generate_terms(expr_number):
    if expr_number > 15:
        expr_number = expr_number % 15
    while True:
        coeffs = np.zeros(15, dtype=np.int64)
        expr_selector = np.array(
            [random.randint(0, expr_number - 1) for _ in range(expr_number)]
        )
        print(expr_selector)
        # Ax = 0
        A = truth_table[expr_selector, :].T
        print(A)
        b = np.zeros(4)
        n = len(A[0])
        m = len(b)
        X = [Int('x%d' % i) for i in range(n)]

        s = Solver()
        # Solution cannot be zero vector 
        s.add(And([X[i] != 0 for i in range(n)]))
        # Force elements to be nonzero to prevent
        # "lame" solutions like [0, 0, 0, ..., 1, 0]
        for i in range(n):
            s.add(X[i] != 0)
        # Constraints for matrix mult
        for i in range(m):
            s.add(Sum([A[i][j] * X[j] for j in range(n)]) == b[i])

        if s.check() == sat:
            # We found a solution! 
            m = s.model()
            # Might not be in order so need to sort by name first
            sol = [m[i] for i in sorted(m, key=lambda x: x.name())]
            for i in range(expr_number):
                coeffs[expr_selector[i]] += int(sol[i].as_string())
            print(coeffs)
            return coeffs

class VariableCounter(cst.CSTVisitor):

    def __init__(self):
        self.count = 0
    
    def visit_Name(self, node: cst.Name):
        self.count += 1

    def visit_Integer(self, node: cst.Name):
        self.count += 1


def count_vars(node: cst.BinaryOperation):
    counter = VariableCounter()
    # Hack solution 
    node_as_str = cst.parse_module("").code_for_node(node)
    node_as_module = cst.parse_module(node_as_str)
    node_as_module.visit(counter)
    num_vars = counter.count
    return num_vars
"""

"""
class LinearMBA(cst.CSTTransformer):
    def leave_BinaryOperation(
        self,
        original_node: cst.BinaryOperation,
        updated_node: cst.BinaryOperation
    ) -> cst.BinaryOperation:
        terms_to_edit = None
        if isinstance(original_node.operator, cst.Add):
            terms_to_edit = [(2, 1), (4, 1)]
        elif isinstance(original_node.operator, cst.Subtract):
            terms_to_edit = [(2, 1), (4, -1)]
        elif isinstance(original_node.operator, cst.BitXor):
            terms_to_edit = [(5, 1)]
        elif isinstance(original_node.operator, cst.BitAnd):
            terms_to_edit = [(0, 1)]
        elif isinstance(original_node.operator, cst.BitOr):
            terms_to_edit = [(6, 1)]
        if terms_to_edit is None:
            return updated_node
        # TODO: Replace with matcher-based solution
        if (
            # Handle list case
            isinstance(original_node.left, cst.List)
            or isinstance(original_node.right, cst.List)
            # Hack case where we have func(x)*2 because this breaks PatchReturn
            # TODO: Investigate and fix root issue 
            or isinstance(original_node.right, cst.Call)
            or isinstance(original_node.left, cst.Call)
            or isinstance(original_node.left, cst.UnaryOperation)
            or isinstance(original_node.left, cst.UnaryOperation)
            # Don't transform UnaryOperations so we can repeatedly apply 
            # transforms without breaking 
        ):
            return updated_node
        count = count_vars(original_node)
        print()
        if count > 1:
            terms = generate_terms(count+5)
        else:
            return updated_node
        for idx, val in terms_to_edit:
            terms[idx] += val
        result = []
        for i in range(15):
            expression = func_list[i](x=original_node.left, y=original_node.right)
            # For some reason libCST won't let us do Integer(-1) 
            if terms[i] != 0:
                if terms[i] >= 0:
                    result.append(
                        cst.BinaryOperation(
                            left=cst.Integer(
                                value=str(terms[i]),
                                lpar=[cst.LeftParen()],
                                rpar=[cst.RightParen()]
                            ),
                            operator=cst.Multiply(),
                            right=expression,
                            lpar=[cst.LeftParen()],
                            rpar=[cst.RightParen()]
                        )
                    )
                # Make this a UnaryOperation with Minus to make -1 
                else:
                    result.append(
                        cst.BinaryOperation(
                            left=cst.UnaryOperation(
                                operator=cst.Minus(),
                                expression=cst.Integer(
                                    value=str(terms[i])[1:],
                                ),
                                lpar=[cst.LeftParen()],
                                rpar=[cst.RightParen()]
                            ),
                            operator=cst.Multiply(),
                            right=expression,
                            lpar=[cst.LeftParen()],
                            rpar=[cst.RightParen()]
                        )
                    )
        # Now we have to construct the resulting expression from the array
        result = " + ".join(cst.parse_module("").code_for_node(expr) for expr in result)          
        result = "(" + result + ")"
        print("="*100)
        print(f"count: {count}")
        print(cst.parse_module("").code_for_node(original_node))
        print(result)
        print("="*100)

        result = cst.parse_expression(result)
        return updated_node.with_changes(
            left=result.left,
            operator=result.operator,
            right=result.right,
            lpar=[cst.LeftParen()],
            rpar=[cst.RightParen()]
        )
"""

