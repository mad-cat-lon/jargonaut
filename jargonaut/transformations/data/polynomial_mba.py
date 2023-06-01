import libcst as cst 


def zeroeq_polynomial_mba(expression):
    """
    Generates a strong polynomial MBA from a given expression
    using a 0-equality 
    """
    # Let E_1 be an expression
    # Let E_2 and E_m_2 be linear MBA expressions 
    # The coefficients of E_1 are randomly reversed to construct a new expression E_m_1 
    # A sub-expression of E_2 forms part of E_m_2 and E_m_2 = 0
    # Then E_1 * E_2's 0-equality is Z = E_m_1 * E_m_2 = 0 
    node = cst.BinaryOperation()
    return node