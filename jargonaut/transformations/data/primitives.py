import libcst as cst


def x_and_y(x, y):
    """
    x & y
    """
    return cst.BinaryOperation(
        left=x,
        operator=cst.BitAnd(),
        right=y,
        lpar=[cst.LeftParen()],
        rpar=[cst.RightParen()]
    )


def x_and_not_y(x, y):
    """
    x & ~y
    """
    return cst.BinaryOperation(
        left=x,
        operator=cst.BitAnd(),
        right=cst.UnaryOperation(
            operator=cst.BitInvert(),
            expression=y
        ),
        lpar=[cst.LeftParen()],
        rpar=[cst.RightParen()]
    )


def x(x, y=None):
    """
    x 
    """
    return x


def not_x_and_y(x, y):
    """
    ~x & y
    """
    return cst.BinaryOperation(
        left=cst.UnaryOperation(
            operator=cst.BitInvert(),
            expression=x
        ),
        operator=cst.BitAnd(),
        right=y,
        lpar=[cst.LeftParen()],
        rpar=[cst.RightParen()]
    )


def y(y, x=None):
    """
    y
    """
    return y


def x_xor_y(x, y):
    """
    x ^ y
    """
    return cst.BinaryOperation(
        left=x,
        operator=cst.BitXor(),
        right=y,
        lpar=[cst.LeftParen()],
        rpar=[cst.RightParen()]
    )


def x_or_y(x, y):
    """
    x | y
    """
    return cst.BinaryOperation(
        left=x,
        operator=cst.BitOr(),
        right=y,
        lpar=[cst.LeftParen()],
        rpar=[cst.RightParen()]
    )


def not_inc_x_or_y(x, y):
    """
    ~(x | y)
    """
    return cst.UnaryOperation(
        operator=cst.BitInvert(),
        expression=cst.BinaryOperation(
            left=x,
            operator=cst.BitOr(),
            right=y,
            lpar=[cst.LeftParen()],
            rpar=[cst.RightParen()]
        ),
    )


def not_inc_x_xor_y(x, y):
    """
    ~(x ^ y)
    """
    return cst.UnaryOperation(
        operator=cst.BitInvert(),
        expression=cst.BinaryOperation(
            left=x,
            operator=cst.BitXor(),
            right=y,
            lpar=[cst.LeftParen()],
            rpar=[cst.RightParen()]
        )
    )


def not_y(y, x=None):
    """
    ~y
    """
    return cst.UnaryOperation(
        operator=cst.BitInvert(),
        expression=y
    )


def x_or_not_y(x, y):
    """
    x | ~ y
    """
    return cst.BinaryOperation(
        left=x,
        operator=cst.BitOr(),
        right=cst.UnaryOperation(
            operator=cst.BitInvert(),
            expression=y
        ),
        lpar=[cst.LeftParen()],
        rpar=[cst.RightParen()]
    )


def not_x(x, y=None):
    """
    ~x
    """
    return cst.UnaryOperation(
        operator=cst.BitInvert(),
        expression=y
    )


def not_x_or_y(x, y):
    """
    ~x | y
    """
    return cst.BinaryOperation(
        left=cst.UnaryOperation(
            operator=cst.BitInvert(),
            expression=x
        ),
        operator=cst.BitOr(),
        right=y,
        lpar=[cst.LeftParen()],
        rpar=[cst.RightParen()]
    )


def not_inc_x_and_y(x, y):
    """
    ~(x & y)
    """
    return cst.UnaryOperation(
        operator=cst.BitInvert(),
        expression=cst.BinaryOperation(
            left=x,
            operator=cst.BitAnd(),
            right=y
        )
    )


def min_one(x=None, y=None):
    """
    -1
    """
    return cst.UnaryOperation(
        operator=cst.Minus(),
        expression=cst.Integer("1")
    )