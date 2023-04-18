from z3 import Int, Sum, And, Solver, sat
import numpy as np
import ast
import random 


def x_and_y(x, y):
    return ast.Expr(
        value=ast.BoolOp(
            op=ast.And(),
            values=[
                ast.Name(id=x, ctx=ast.Load()),
                ast.Name(id=y, ctx=ast.Load())
            ]
        )
    )

def x_and_not_y(x, y):
    return ast.Expr(
        value=ast.BoolOp(
            op=ast.And(),
            values=[
                ast.Name(id=x, ctx=ast.Load()),
                ast.UnaryOp(
                    op=ast.Not(),
                    operand=ast.Name(id=y, ctx=ast.Load()))
            ]
        )
    )

def x(x, y=None):
    return ast.Expr(
        value=ast.Name(id=x, ctx=ast.Load())
    )

def not_x_and_y(x, y):
    return ast.Expr(
    value=ast.BoolOp(
        op=ast.And(),
        values=[
            ast.UnaryOp(
                op=ast.Not(),
                operand=ast.Name(id=x, ctx=ast.Load())),
            ast.Name(id=y, ctx=ast.Load())
        ]
    )
)

def y(y, x=None):
    return ast.Expr(
        value=ast.Name(id=y, ctx=ast.Load())
    )

def x_xor_y(x, y):
    return ast.Expr(
        value=ast.BinOp(
            left=ast.Name(id=x, ctx=ast.Load()),
            op=ast.BitXor(),
            right=ast.Name(id=y, ctx=ast.Load())
        )
    )

def x_or_y(x, y):
    return ast.Expr(
        value=ast.BoolOp(
            op=ast.Or(),
            values=[
                ast.Name(id=x, ctx=ast.Load()),
                ast.Name(id=y, ctx=ast.Load())
            ]
        )
    )

def not_inc_x_or_y(x, y):
    return ast.Expr(
        value=ast.UnaryOp(
            op=ast.Not(),
            operand=ast.BoolOp(
                op=ast.Or(),
                values=[
                    ast.Name(id=x, ctx=ast.Load()),
                    ast.Name(id=y, ctx=ast.Load())
                ]
            )
        )
    )

def not_inc_x_xor_y(x, y):
    return ast.Expr(
        value=ast.UnaryOp(
            op=ast.Not(),
            operand=ast.BinOp(
                left=ast.Name(id=x, ctx=ast.Load()),
                op=ast.BitXor(),
                right=ast.Name(id=y, ctx=ast.Load())
            )
        )
    )

def not_y(y, x=None):
    return ast.Expr(
        value=ast.UnaryOp(
            op=ast.Not(),
            operand=ast.Name(id=y, ctx=ast.Load())
        )
    )

def x_or_not_y(x, y):
    return ast.Expr(
        value=ast.BoolOp(
            op=ast.Or(),
            values=[
                ast.Name(id=x, ctx=ast.Load()),
                ast.UnaryOp(
                    op=ast.Not(),
                    operand=ast.Name(id=y, ctx=ast.Load())
                )
            ]
        )
    )

def not_x(x, y=None):
    return ast.Expr(
        value=ast.UnaryOp(
            op=ast.Not(),
            operand=ast.Name(id=x, ctx=ast.Load())
        )
    )

def not_x_or_y(x, y):
    return ast.Expr(
        value=ast.BoolOp(
            op=ast.Or(),
            values=[
                ast.UnaryOp(
                    op=ast.Not(),
                    operand=ast.Name(id=x, ctx=ast.Load())
                ),
                ast.Name(id=y, ctx=ast.Load())
            ]
        )
    )

def not_inc_x_and_y(x, y):
    return ast.Expr(
        value=ast.UnaryOp(
            op=ast.Not(),
            operand=ast.BoolOp(
                op=ast.And(),
                values=[
                    ast.Name(id=x, ctx=ast.Load()),
                    ast.Name(id=y, ctx=ast.Load())
                ]
            )
        )
    )


def min_one(x=None, y=None):
    return ast.Expr(
        value=ast.Constant(-1)
    )

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
    x_and_y,
    x_and_not_y,
    x,
    not_x_and_y,
    y,
    x_xor_y,
    x_or_y,
    not_inc_x_or_y,
    not_inc_x_xor_y,
    not_y,
    x_or_not_y,
    not_x,
    not_x_or_y,
    not_inc_x_and_y,
    min_one
]

def generate_terms(expr_number):
    while True:
        coeffs = np.zeros(15, dtype=np.int64)
        expr_selector = np.array(
            [random.randint(0, expr_number-1) for _ in range(expr_number)]
        )
        A = truth_table[expr_selector, :].T
        b = np.zeros(4)
        n = len(A[0])
        m = len(b)
        X = [Int('x%d' % i) for i in range(n)]

        s = Solver()
        s.add(And([X[i] != 0 for i in range(n)]))


        for i in range(m):
            s.add(Sum([A[i][j]*X[j] for j in range(n)]) == b[i])

        if s.check() == sat:
            print(f"expr_selector: {expr_selector}")
            # We found a solution! 
            m = s.model()
            sol = [m[i] for i in sorted(m, key=lambda x: x.name())]
            print(f"SAT solver found a solution: {sol}")
            for i in range(expr_number):
                print(f"i: {i} expr_selector[i]: {expr_selector[i]} sol[i]: {sol[i].as_string()}")
                coeffs[expr_selector[i]] += int(sol[i].as_string())
            return coeffs

def generate_linear_mba(terms: list, expr: ast.BinOp):
    final_expr = []
    primitive_expr = None
    # Just doing add for now 
    x = expr.left.id
    y = expr.right.id
    for i in range(15):
        primitive_expr = func_list[i](x=x, y=y)
        print(f"{ast.dump(primitive_expr)} >> {ast.unparse(primitive_expr)}")
        final_expr.append(f"({terms[i]})*({ast.unparse(primitive_expr)})")
    final_expr = '+'.join(final_expr)
    print(final_expr)

if __name__ == "__main__":
    coeffs = generate_terms(6)
