from ..unicloak import Unicloak
import ast 


def test_smoke():
    in_file = """
def op(x):
    a = 2 
    b = 5
    c = a + b + 1
    d = c * x
    return d * 2

print(op(3))
    """
    uc = Unicloak()
    tree = ast.parse(in_file)
    uc.visit(tree)
    out_file = ast.unparse(tree)
    
    p1 = exec(in_file)
    p2 = exec(out_file)

    assert p1 == p2

