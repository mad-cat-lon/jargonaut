import ast 
import unicloak.transformations.data.primitives as primitives
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
      

class LinearMBA(ast.NodeTransformer):
    """
    Converts constants and binary operations into linear 
    mixed boolean arithmetic expressions 
    """
    def __init__(self, avoid=[], keys=["1337", "1984", "999", "747", "31415", "420"]):
        self.avoid = avoid
        self.keys = keys
        self.msg = "Replacing expressions and constants with MBA..."
    
    def visit_BinOp(self, node: ast.BinOp):
        """
        Generates linear MBA for BinOp nodes.
        """
        final_expr = []
        primitive_expr = None
        # I should really be updating to 3.10 and use match here
        terms_to_edit = None
        if isinstance(node.op, ast.Add):
            terms_to_edit = [(2, 1), (4, 1)]
        elif isinstance(node.op, ast.Sub):
            terms_to_edit = [(2, 1), (4, -1)]
        elif isinstance(node.op, ast.BitXor):
            terms_to_edit = [(5, 1)]
        elif isinstance(node.op, ast.BitAnd):
            terms_to_edit = [(0, 1)]
        elif isinstance(node.op, ast.BitOr):
            terms_to_edit = [(6, 1)]

        if (
            isinstance(node.left, ast.Name)
            and isinstance(node.right, ast.Name)
        ):
            terms = generate_terms(NUM_TERMS)
            # Find which indices we need to edit to balance equation
            if terms_to_edit is None:
                return node
            for idx, val in terms_to_edit:
                terms[idx] += val
            x = node.left.id
            y = node.right.id
            for i in range(15):
                primitive_expr = func_list[i](x=x, y=y)
                if terms[i] != 0:
                    final_expr.append(
                        f"({terms[i]})*({ast.unparse(primitive_expr)})"
                    )
                    # print(f"{ast.dump(primitive_expr)}>>{ast.unparse(primitive_expr)}")
            final_expr = '+'.join(final_expr)
            return ast.parse(final_expr).body[0].value
        else:
            return node
    
    def visit_Constant(self, node: ast.Constant):
        """
        Generates linear MBA for ast.Constant nodes
        """
        if isinstance(node.value, int):
            final_expr = []
            primitive_expr = None
            terms = generate_terms(NUM_TERMS)
            terms[14] -= int(node.value)
            # Placeholder terms for now 
            x, y = random.sample(self.keys, 2)
            for i in range(15):
                primitive_expr = func_list[i](x=x, y=y)
                if terms[i] != 0:
                    final_expr.append(
                        f"({terms[i]})*({ast.unparse(primitive_expr)})"
                    )
            final_expr = '+'.join(final_expr)
            return ast.parse(final_expr).body[0].value
        return node