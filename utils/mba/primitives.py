import ast


def x_and_y(x, y):
    """
    x & y
    """
    return ast.Expr(
        value=ast.BinOp(
            left=ast.Name(id=x, ctx=ast.Load()),
            op=ast.BitAnd(),
            right=ast.Name(id=y, ctx=ast.Load())
        )
    )


def x_and_not_y(x, y):
    """
    x & ~y
    """
    return ast.Expr(
        value=ast.BinOp(
            left=ast.Name(id=x, ctx=ast.Load()),
            op=ast.BitAnd(),
            right=ast.UnaryOp(
                op=ast.Invert(),
                operand=ast.Name(id=y, ctx=ast.Load())
            )
        )
    )


def x(x, y=None):
    """
    x 
    """
    return ast.Expr(
        value=ast.Name(id=x, ctx=ast.Load())
    )


def not_x_and_y(x, y):
    """
    ~x & y
    """
    return ast.Expr(
        value=ast.BinOp(
            left=ast.UnaryOp(
                op=ast.Invert(),
                operand=ast.Name(id=x, ctx=ast.Load())
            ),
            op=ast.BitAnd(),
            right=ast.Name(id=y, ctx=ast.Load())
        )
    )


def y(y, x=None):
    """
    y
    """
    return ast.Expr(
        value=ast.Name(id=y, ctx=ast.Load())
    )


def x_xor_y(x, y):
    """
    x ^ y
    """
    return ast.Expr(
        value=ast.BinOp(
            left=ast.Name(id=x, ctx=ast.Load()),
            op=ast.BitXor(),
            right=ast.Name(id=y, ctx=ast.Load())
        )
    )


def x_or_y(x, y):
    """
    x | y
    """
    return ast.Expr(
        value=ast.BinOp(
            left=ast.Name(id=x, ctx=ast.Load()),
            op=ast.BitOr(),
            right=ast.Name(id=y, ctx=ast.Load())
        )
    )


def not_inc_x_or_y(x, y):
    """
    ~(x | y)
    """
    return ast.Expr(
        value=ast.UnaryOp(
            op=ast.Invert(),
            operand=ast.BinOp(
                left=ast.Name(id=x, ctx=ast.Load()),
                op=ast.BitOr(),
                right=ast.Name(id=y, ctx=ast.Load())
            )
        )
    )


def not_inc_x_xor_y(x, y):
    """
    ~(x ^ y)
    """
    return ast.Expr(
        value=ast.UnaryOp(
            op=ast.Invert(),
            operand=ast.BinOp(
                left=ast.Name(id=x, ctx=ast.Load()),
                op=ast.BitXor(),
                right=ast.Name(id=y, ctx=ast.Load())
            )
        )
    )


def not_y(y, x=None):
    """
    ~y
    """
    return ast.Expr(
        value=ast.UnaryOp(
            op=ast.Invert(),
            operand=ast.Name(id=y, ctx=ast.Load())
        )
    )


def x_or_not_y(x, y):
    """
    x | ~ y
    """
    return ast.Expr(
        value=ast.BinOp(
            left=ast.Name(id=x, ctx=ast.Load()),
            op=ast.BitOr(),
            right=ast.UnaryOp(
                op=ast.Invert(),
                operand=ast.Name(id=y, ctx=ast.Load())
            )

        )
    )


def not_x(x, y=None):
    """
    ~x
    """
    return ast.Expr(
        value=ast.UnaryOp(
            op=ast.Invert(),
            operand=ast.Name(id=x, ctx=ast.Load())
        )
    )


def not_x_or_y(x, y):
    """
    ~x | y
    """
    return ast.Expr(
        value=ast.BinOp(
            left=ast.UnaryOp(
                op=ast.Invert(),
                operand=ast.Name(id=x, ctx=ast.Load())
            ),
            op=ast.BitOr(),
            right=ast.Name(id=x, ctx=ast.Load())
        )
    )


def not_inc_x_and_y(x, y):
    """
    ~(x & y)
    """
    return ast.Expr(
        value=ast.UnaryOp(
            op=ast.Invert(),
            operand=ast.BinOp(
                left=ast.Name(id=x, ctx=ast.Load()),
                op=ast.BitAnd(),
                right=ast.Name(id=y, ctx=ast.Load())
            )
        )
    )


def min_one(x=None, y=None):
    """
    -1
    """
    return ast.Expr(
        value=ast.Constant(-1)
    )
