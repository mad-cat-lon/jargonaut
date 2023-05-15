import libcst as cst
import jargonaut.transformations.data.primitives as primitives
import numpy as np
import random 
from z3 import Int, Sum, And, Solver, sat

"""
References:
https://theses.hal.science/tel-01623849/document
https://bbs.kanxue.com/thread-271574.htm
"""

NUM_TERMS = 10

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
    while True:
        coeffs = np.zeros(15, dtype=np.int64)
        expr_selector = np.array(
            [random.randint(0, expr_number - 1) for _ in range(expr_number)]
        )
        # Ax = 0
        A = truth_table[expr_selector, :].T
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
            return coeffs
        

class LinearMBA(cst.CSTTransformer):
    """
    Converts constants and binary operations into linear mixed boolean arithmetic expressions
    """
    def __init__(self):
        self.keys = ["1337", "1984", "999", "747", "31415", "420"]
    
    def leave_BinaryOperation(
        self, 
        original_node: cst.BinaryOperation,
        updated_node: cst.BinaryOperation
    ) -> None:
        """
        Generates linear MBA for binary operations
        """
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
        if (
            isinstance(original_node.left, cst.Name)
            and isinstance(original_node.right, cst.Name)
        ):
            if terms_to_edit is None:
                return original_node
            terms = generate_terms(NUM_TERMS)
            for idx, val in terms_to_edit:
                terms[idx] += val
            result = []
            for i in range(15):
                expression = func_list[i](x=original_node.left, y=original_node.right)
                if terms[i] != 0:
                    # For some reason libCST won't let us do Integer(-1) 
                    if terms[i] > 0:
                        result.append(
                            cst.BinaryOperation(
                                left=cst.Integer(str(terms[i])),
                                operator=cst.Multiply(),
                                right=expression
                            )
                        )
                    else:
                        result.append(
                            cst.BinaryOperation(
                                left=cst.UnaryOperation(
                                    operator=cst.Minus(),
                                    expression=cst.Integer(str(terms[i])[1:])
                                ),
                                operator=cst.Multiply(),
                                right=expression
                            )
                        )
            # Now we have to construct the resulting expression from the array
            result = " + ".join(cst.parse_module("").code_for_node(expr) for expr in result)          
            result = cst.parse_expression(result)
            return updated_node.with_changes(
                left=result.left,
                operator=result.operator,
                right=result.right,
                lpar=[cst.LeftParen()],
                rpar=[cst.RightParen()]
            )
        return updated_node

    def leave_Integer(
        self,
        original_node: cst.Integer,
        updated_node: cst.Integer
    ):
        terms = generate_terms(NUM_TERMS)
        terms[14] -= original_node.evaluated_value
        x, y = random.sample(self.keys, 2)
        x = cst.Integer(x)
        y = cst.Integer(y)
        result = []
        for i in range(15):
            expression = func_list[i](x=x, y=y)
            if terms[i] != 0:
                if terms[i] > 0:
                    result.append(
                        cst.BinaryOperation(
                            left=cst.Integer(str(terms[i])),
                            operator=cst.Multiply(),
                            right=expression
                        )
                    )
                else:
                    result.append(
                        cst.BinaryOperation(
                            left=cst.UnaryOperation(
                                operator=cst.Minus(),
                                expression=cst.Integer(str(terms[i])[1:])
                            ),
                            operator=cst.Multiply(),
                            right=expression
                        )
                    )
        result = " + ".join(cst.parse_module("").code_for_node(expr) for expr in result)       
        result = cst.parse_expression(result)
        result = cst.BinaryOperation(
            left=result.left,
            operator=result.operator,
            right=result.right,
            lpar=[cst.LeftParen()],
            rpar=[cst.RightParen()]
        )
        return result
        