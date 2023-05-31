import libcst as cst
# import jargonaut.transformations.data.primitives as primitives
# import numpy as np
import random 
# from z3 import Int, Sum, And, Solver, sat
from libcst.metadata import ParentNodeProvider, TypeInferenceProvider, PositionProvider
from libcst.metadata import ScopeProvider
from .mba_utils import rewrite_expr, constant_to_mba


class ExprToLinearMBA(cst.CSTTransformer):
    """
    Converts constants and binary operations into linear mixed boolean arithmetic expressions
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
        self.progress_msg = "[-] Obfuscating expressions with linear MBA expressions..."
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

    def leave_Integer(
        self,
        original_node: cst.Integer,
        updated_node: cst.Integer
    ):
        if self.inference:
            constant_mba = constant_to_mba(
                original_node.evaluated_value,
                as_obj=False
            )
            scope = self.get_metadata(ScopeProvider, original_node)
            # Let's check if there are any integer variables in the scope we can use for confusion
            assignments_in_scope = []
            for assign in scope.assignments:
                # Only take Name() for now
                if isinstance(assign.node, cst.Name):
                    # Check if it's in scope
                    if assign.node.value in scope:
                        node_pos = self.get_metadata(PositionProvider, original_node).start 
                        assign_pos = self.get_metadata(PositionProvider, assign.node).start
                        # HACK: Don't use the assignment unless it appears before our current node
                        if node_pos.line > assign_pos.line:
                            assignments_in_scope.append(assign.node)
            # Do type inferencing here to find Name() nodes that are of type int
            int_names = []
            for node in assignments_in_scope:
                # HACK: When we run PatchReturns() before this transformation,
                # we insert a Name(value="frame") to do the patching
                # Pyre doesn't know about this yet so we need to handle the KeyError
                try:
                    inferred_type = self.get_metadata(TypeInferenceProvider, node)
                    if inferred_type == "int":
                        int_names.append(node)
                except KeyError:
                    pass 
            if int_names:
                # Replace x and y in the constant_mba expression
                x = random.choice(int_names)
                y = random.choice(int_names)
                constant_mba = constant_mba.replace("x", x.value)
                constant_mba = constant_mba.replace("y", y.value)
                return cst.parse_expression(constant_mba)
            else:
                # print("No names found, inserting statements")
                # We have a few options here
                # 1. Just use random integers for x and y
                # 2. Define integer vars before the expression 
                # 3. If inside a function, add parameters and edit all calls to include vars
                # HACK: Doing option 1 for now: inserting statements before a node is finicky 
                # x_name = ''.join([random.choice("abcdefghihklmnopqrstuv") for _ in range(10)])
                # y_name = ''.join([random.choice("abcdefghihklmnopqrstuv") for _ in range(10)])
                x_val = random.randint(0, 1000)
                y_val = random.randint(0, 1000)
                constant_mba = constant_mba.replace("x", str(x_val))
                constant_mba = constant_mba.replace("y", str(y_val))
                return cst.parse_expression(constant_mba)
        else:
            constant_mba = constant_to_mba(
                int(original_node.evaluated_value),
                as_obj=False
            )
            x_val = random.randint(0, 1000)
            y_val = random.randint(0, 1000)
            constant_mba = constant_mba.replace("x", str(x_val))
            constant_mba = constant_mba.replace("y", str(y_val))
            return cst.parse_expression(constant_mba)
            """
            x_assign = cst.Assign(
                targets=[
                    cst.AssignTarget(
                        target=cst.Name(
                            value=x_name
                        )
                    )
                ],
                value=cst.Integer(
                    value=str(x_val)
                )
            )
            y_assign = cst.Assign(
                targets=[
                    cst.AssignTarget(
                        target=cst.Name(
                            value=y_name
                        )
                    )
                ],
                value=cst.Integer(
                    value=str(y_val)
                )
            )
            return cst.FlattenSentinel([x_assign, y_assign, cst.parse_expression(constant_mba)])
            """
        return original_node


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

