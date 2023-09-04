from jargonaut.transformations.data.mba_utils import constant_to_mba
import random
import libcst as cst

def generate_mba_expr(value, int_names=None):
    """
    Generates an MBA (Mixed Boolean Arithmetic) expression based on the given value and variable names.
    
    Parameters:
    - value (int): The constant value to be converted into an MBA expression.
    - int_names (list): Optional list of variable names to be used in the MBA expression.
    
    Returns:
    - str: The generated MBA expression as a string.
    """
    mba_expr = constant_to_mba(value, n_terms=random.randint(4, 7), as_obj=False)
    
    if int_names:
        x = random.choice(int_names)
        y = random.choice(int_names)
        mba_expr = mba_expr.replace("x", x.value).replace("y", y.value)
    else:
        x_val = random.randint(0, 1000)
        y_val = random.randint(0, 1000)
        mba_expr = mba_expr.replace("x", str(x_val)).replace("y", str(y_val))
    
    return mba_expr

def generate_static_mba_eq_pred(as_obj=True, int_names=[]):
    """
    Generates a static opaque predicate using an equality check with MBA expressions.
    
    Parameters:
    - as_obj (bool): Determines if the output should be an object or a string.
    - int_names (list): Optional list of variable names to be used in the MBA expression.
    
    Returns:
    - cst.BaseExpression or str: The generated predicate as an object or a string.
    """
    pred_int = random.randint(0, 10000)
    left_mba_expr = generate_mba_expr(pred_int, int_names)
    right_mba_expr = generate_mba_expr(pred_int, int_names)
    
    mba_pred = f"{left_mba_expr} == {right_mba_expr}"
    
    return cst.parse_expression(mba_pred) if as_obj else mba_pred

def generate_static_mba_mod_pred(as_obj=True, int_names=[]):
    """
    Generates a static opaque predicate using a modulo operation with MBA expressions.
    
    Parameters:
    - as_obj (bool): Determines if the output should be an object or a string.
    - int_names (list): Optional list of variable names to be used in the MBA expression.
    
    Returns:
    - cst.BaseExpression or str: The generated predicate as an object or a string.
    """
    a, n = random.randint(0, 10000), random.randint(0, 10000)
    r = a % n
    
    a_mba_expr = generate_mba_expr(a, int_names)
    n_mba_expr = generate_mba_expr(n, int_names)
    r_mba_expr = generate_mba_expr(r, int_names)
    
    mba_pred = f"{a_mba_expr} % {n_mba_expr} == {r_mba_expr}"
    
    return cst.parse_expression(mba_pred) if as_obj else mba_pred
