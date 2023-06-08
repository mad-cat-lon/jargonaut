from jargonaut.transformations.data.mba_utils import constant_to_mba
import random 
import libcst as cst


def generate_static_mba_equality_pred(as_obj=True):
    """
    Generates a static opaque predicate using equality check with MBA expressions
    """
    
    # TODO: Add option to reuse int variables in scope

    pred_int = random.randint(-1000, 1000)

    left_mba_expr = constant_to_mba(pred_int, n_terms=random.randint(4, 7), as_obj=False)
    left_x_val = random.randint(0, 1000)
    left_y_val = random.randint(0, 1000)
    left_mba_expr = left_mba_expr.replace("x", str(left_x_val))
    left_mba_expr = left_mba_expr.replace("y", str(left_y_val))

    right_mba_expr = constant_to_mba(pred_int, n_terms=random.randint(4, 7), as_obj=False)
    right_x_val = random.randint(0, 1000)
    right_y_val = random.randint(0, 1000)
    right_mba_expr = right_mba_expr.replace("x", str(right_x_val))
    right_mba_expr = right_mba_expr.replace("y", str(right_y_val))
    
    mba_pred = f"{left_mba_expr} == {right_mba_expr}"
    if as_obj:
        return cst.parse_expression(mba_pred)
    else:
        return mba_pred