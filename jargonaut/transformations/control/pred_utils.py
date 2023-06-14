from jargonaut.transformations.data.mba_utils import constant_to_mba
import random 
import libcst as cst


def generate_static_mba_eq_pred(as_obj=True, int_names=[]):
    """
    Generates a static opaque predicate using equality check with MBA expressions
    """
    pred_int = random.randint(0, 10000)
    if int_names:
        left_mba_expr = constant_to_mba(pred_int, n_terms=random.randint(4, 7), as_obj=False)
        left_x = random.choice(int_names)
        left_y = random.choice(int_names)
        left_mba_expr = left_mba_expr.replace("x", left_x.value)
        left_mba_expr = left_mba_expr.replace("y", left_y.value)

        right_mba_expr = constant_to_mba(pred_int, n_terms=random.randint(4, 7), as_obj=False)
        right_x = random.choice(int_names)
        right_y = random.choice(int_names)
        right_mba_expr = right_mba_expr.replace("x", right_x.value)
        right_mba_expr = right_mba_expr.replace("y", right_y.value)  
    else:
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


def generate_static_mba_mod_pred(as_obj=True, int_names=[]):
    a = random.randint(0, 10000)
    n = random.randint(0, 10000)
    r = a % n
    print(f"{a} % {n} == {r}")    
    if int_names:
        a_mba_expr = constant_to_mba(a, n_terms=random.randint(4, 7), as_obj=False)
        a_x = random.choice(int_names)
        a_y = random.choice(int_names)
        a_mba_expr = a_mba_expr.replace("x", a_x.value)
        a_mba_expr = a_mba_expr.replace("y", a_y.value)

        n_mba_expr = constant_to_mba(n, n_terms=random.randint(4, 7), as_obj=False)
        n_x = random.choice(int_names)
        n_y = random.choice(int_names)
        n_mba_expr = n_mba_expr.replace("x", n_x.value)
        n_mba_expr = n_mba_expr.replace("y", n_y.value)

        r_mba_expr = constant_to_mba(r, n_terms=random.randint(4, 7), as_obj=False)
        r_x = random.choice(int_names)
        r_y = random.choice(int_names)
        r_mba_expr = n_mba_expr.replace("x", r_x.value)
        r_mba_expr = n_mba_expr.replace("y", r_y.value)
    else:
        a_mba_expr = constant_to_mba(a, n_terms=random.randint(4, 7), as_obj=False)
        a_x_val = random.randint(0, 1000)
        a_y_val = random.randint(0, 1000)
        a_mba_expr = a_mba_expr.replace("x", str(a_x_val))
        a_mba_expr = a_mba_expr.replace("y", str(a_y_val))

        n_mba_expr = constant_to_mba(n, n_terms=random.randint(4, 7), as_obj=False)
        n_x_val = random.randint(0, 1000)
        n_y_val = random.randint(0, 1000)
        n_mba_expr = n_mba_expr.replace("x", str(n_x_val))
        n_mba_expr = n_mba_expr.replace("y", str(n_y_val))

        r_mba_expr = constant_to_mba(r, n_terms=random.randint(4, 7), as_obj=False)
        r_x = random.choice(int_names)
        r_y = random.choice(int_names)
        r_mba_expr = n_mba_expr.replace("x", r_x.value)
        r_mba_expr = n_mba_expr.replace("y", r_y.value)
    mba_pred = f"{a_mba_expr} % {n_mba_expr} == {r_mba_expr}"
    if as_obj:
        return cst.parse_expression(mba_pred)
    else:
        return mba_pred
