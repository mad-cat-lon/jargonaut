import z3 
import numpy as np
import random
import libcst as cst 
import platform 
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
    # Prevent clashes in case source uses the same var name as the expression
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


def generate_zero_identity_mba(t):
    """
    Generates a linear MBA expression of t variables that always evaluates to 0 
    for any x, y in Z
    t MUST be >= 4
    """
    expr_to_truthtable = {
        "(x & y)":    [0, 0, 0, 1],
        "(x & ~y)":   [0, 0, 1, 0],
        "(x)":        [0, 0, 1, 1],
        "(~x & y)":   [0, 1, 0, 0],
        "(y)":        [0, 1, 0, 1],
        "(x ^ y)":    [0, 1, 1, 0],
        "(x | y)":    [0, 1, 1, 1],
        "(~(x | y))": [1, 0, 0, 0],
        "(~(x ^ y))": [1, 0, 0, 1],
        "(~y)":       [1, 0, 1, 1],
        "(x | ~y)":   [1, 0, 1, 1],
        "(~x)":       [1, 1, 0, 0],
        "(~x | y)":   [1, 1, 0, 1],
        "(~(x & y))": [1, 1, 1, 0],
        "(-1)":       [1, 1, 1, 1]
    }
    truthtable_to_expr = {
        tuple(truthtable): expr
        for expr, truthtable in expr_to_truthtable.items()
    }
    # Theorem 1 in https://theses.hal.science/tel-01623849/document    
    mba_identity = None
    while True:
        col_vecs = random.sample(list(expr_to_truthtable.values()), k=t)
        F = np.column_stack(col_vecs)
        b = np.array([0, 0, 0, 0], dtype=np.int64)
        m, n = F.shape
        # We want to solve for FV=0
        # Represent V as a list of variables that are constrained to ints
        V = [z3.Int("v%d" % i) for i in range(t)]
        solver = z3.Solver()
        # Solution can't be zero vector and we want to avoid solutions like [0, 0, 0, 1]
        for var in V:
            solver.add(var != 0)
        # Matrix multiplication implemented as z3 constraints
        for i in range(m):
            solver.add(z3.Sum([F[i][j] * V[j] for j in range(t)]) == b[i])
        if solver.check() == z3.sat:
            sol = solver.model()
            sorted_sol = [
                int(sol[i].as_string())
                for i in sorted(sol, key=lambda x: x.name())
            ]
            # Just in case my implementation was wrong, let's do a final check 
            sol_as_vec = np.array(sorted_sol, dtype=np.int64).T
            check = np.matmul(F, sol_as_vec)
            # F times solution vector should be zero vector
            if not np.any(check):
                result = []
                # Recover expressions associated with each column to form final MBA
                for idx, vec in enumerate(col_vecs): 
                    vec_as_tuple = tuple(vec)
                    result.append(
                        f"{sol_as_vec[idx]}*{truthtable_to_expr[vec_as_tuple]}"
                    )
                result = "+".join(result)
                # Final check: expression must equal 0 for any x, y
                # Let's just do this test a few times
                test_num = 10
                all_test_results = [False for _ in range(test_num)]
                for i in range(test_num):
                    x = random.randint(0, 100)
                    y = random.randint(0, 100)
                    test_result = result.replace("x", str(x))
                    test_result = test_result.replace("y", str(y))
                    if eval(result) == 0:
                        all_test_results[i] = True
                if all(all_test_results):
                    # Good enough for me!
                    mba_identity = result
                    break
    # print(f"Found 0-identity: {mba_identity}")
    return mba_identity 


def generate_invertible_polynomial():
    """
    Generates an invertible quadratic polynomial:
    p(x) = ax^2 + bx + c where a != 0
    """
    pass 


def generate_invertible_affine(n):
    """
    Generates an invertible affine function over the finite field Z/2^nZ
    f(x) = ax + b where a != 0
    """
    a = random.randrange(1, 2**n, 2)
    b = random.randint(0, 2**n - 1)

    a_inv = pow(a, -1, 2**n)
    b_inv = -a_inv*b % (2**n)
    return (a, b), (a_inv, b_inv)


def constant_to_mba(k, as_obj=True):
    """
    Generates an affine function and zero-identity MBA and produces an 
    equivalent MBA expression node that always evaluates to the target constant k
    """
    zero_id_mba = generate_zero_identity_mba(7)
    # https://sci-hub.se/https://link.springer.com/chapter/10.1007/978-3-540-77535-5_5
    # Page 4, Proposition 2
    # Proposition is for invertible polynomials but should work on affine functions too
    # if p(x) is our affine function and q(x) its inverse, then:
    # p(q(k)) == q(zero_id_mba + p(k))

    # we need to account for variable bit lengths in python
    n = random.randint(k.bit_length(), 100)
    coeffs = generate_invertible_affine(n)
    # Let's build the expression now
    # Make args random strings to prevent clashes
    p_arg = "".join(random.sample("abcdefghijklmnop", k=10))
    q_arg = "".join(random.sample("abcdefghijklmnop", k=10))
    p = f"{coeffs[0][0]}*({p_arg})+({coeffs[0][1]})"
    q = f"{coeffs[1][0]}*({q_arg})+({coeffs[1][1]})"
    p = p.replace(p_arg, str(k))
    # Evaluate p(k) so that the constant doesn't show up in the final expr
    p = str(eval(p))
    q = q.replace(q_arg, f"({zero_id_mba})+({p})")
    constant_mba_expr = f"(({q})%2**{n})"
    if as_obj:
        constant_mba_expr = cst.parse_expression(constant_mba_expr)
        return constant_mba_expr
    else:
        return constant_mba_expr


"""
if __name__ == "__main__":
    base_expr = cst.parse_expression("x + y")
    linear_mba = rewrite_expr(base_expr)
    print("Rewrote expression: ")
    print(f"{cst.parse_module('').code_for_node(base_expr)} -> {cst.parse_module('').code_for_node(linear_mba)}")
    zero_id = generate_zero_identity_mba(t=5)
    constant_to_mba(133334845454)

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
"""
