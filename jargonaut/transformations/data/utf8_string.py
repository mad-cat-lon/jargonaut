import libcst as cst 
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin


class StringToUTF8Int(cst.CSTTransformer):
    """
    Transforms string literals to an integer from UTF8 bytes
    Can handle the escape characters missed by StringToLambdaExpr(),
    the resulting int can also be further obfuscated with MBA expressions
    """
    def __init__(self, avoid=None, probability=1):
        self.avoid = avoid
        self.first_visit = True 
        self.progress_msg = "Obfuscating string literals by encoding to UTF-8 integers..."
        self.spinner = None 
        self.probability = 1

    def encode(self, string):
        string_to_bytes = string.encode('utf-8') + b'\x01' 
        bytes_to_int = int.from_bytes(string_to_bytes, "little")
        return bytes_to_int
    
    def visit_SimpleString(self, node: cst.SimpleString):
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(Spinners.dots12, text=self.progress_msg, timer=True)
            self.spinner.start()
            self.first_visit = False  
        return True
    
    def leave_SimpleString(
        self,
        original_node: cst.SimpleString,
        updated_node: cst.Call
    ) -> cst.Call:
        if (
            len(original_node.value) > 3
            and not original_node.prefix
        ):
            # Skip the quotation marks that appear in the node value
            encoded_string = str(self.encode(original_node.value[1:-1]))
            new_node = cst.Call(
                func=cst.Attribute(
                    value=cst.Subscript(
                        value=cst.Call(
                            func=cst.Attribute(
                                value=cst.Integer(
                                    value=encoded_string,
                                    lpar=[
                                        cst.LeftParen(),
                                    ],
                                    rpar=[
                                        cst.RightParen(),
                                    ],
                                ),
                                attr=cst.Name(
                                    value='to_bytes',
                                    lpar=[],
                                    rpar=[],
                                ),
                                dot=cst.Dot(),
                                lpar=[],
                                rpar=[],
                            ),
                            args=[
                                cst.Arg(
                                    value=cst.BinaryOperation(
                                        left=cst.BinaryOperation(
                                            left=cst.Call(
                                                func=cst.Attribute(
                                                    value=cst.Integer(
                                                        value=encoded_string,
                                                        lpar=[
                                                            cst.LeftParen(),
                                                        ],
                                                        rpar=[
                                                            cst.RightParen(),
                                                        ],
                                                    ),
                                                    attr=cst.Name(
                                                        value='bit_length',
                                                        lpar=[],
                                                        rpar=[],
                                                    ),
                                                    dot=cst.Dot(),
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                args=[],
                                                lpar=[],
                                                rpar=[],
                                            ),
                                            operator=cst.Add(
                                            ),
                                            right=cst.Integer(
                                                value='7',
                                                lpar=[],
                                                rpar=[],
                                            ),
                                            lpar=[
                                                cst.LeftParen(),
                                            ],
                                            rpar=[
                                                cst.RightParen(),
                                            ],
                                        ),
                                        operator=cst.FloorDivide(),
                                        right=cst.Integer(
                                            value='8',
                                            lpar=[],
                                            rpar=[],
                                        ),
                                        lpar=[],
                                        rpar=[],
                                    ),
                                    keyword=None,
                                    equal=cst.MaybeSentinel.DEFAULT,
                                    comma=cst.Comma(),
                                    star=''
                                ),
                                cst.Arg(
                                    value=cst.SimpleString(
                                        value="'little'",
                                        lpar=[],
                                        rpar=[],
                                    ),
                                    keyword=None,
                                    equal=cst.MaybeSentinel.DEFAULT,
                                    comma=cst.MaybeSentinel.DEFAULT,
                                    star=''
                                ),
                            ],
                            lpar=[],
                            rpar=[],
                        ),
                        slice=[
                            cst.SubscriptElement(
                                slice=cst.Slice(
                                    lower=None,
                                    upper=cst.UnaryOperation(
                                        operator=cst.Minus(),
                                        expression=cst.Integer(
                                            value='1',
                                            lpar=[],
                                            rpar=[],
                                        ),
                                        lpar=[],
                                        rpar=[],
                                    ),
                                    step=None,
                                    first_colon=cst.Colon(),
                                    second_colon=cst.MaybeSentinel.DEFAULT,
                                ),
                                comma=cst.MaybeSentinel.DEFAULT,
                            ),
                        ],
                        lbracket=cst.LeftSquareBracket(),
                        rbracket=cst.RightSquareBracket(),
                        lpar=[],
                        rpar=[],

                    ),
                    attr=cst.Name(
                        value='decode',
                        lpar=[],
                        rpar=[],
                    ),
                    dot=cst.Dot(
                        whitespace_before=cst.SimpleWhitespace(
                            value='',
                        ),
                        whitespace_after=cst.SimpleWhitespace(
                            value='',
                        ),
                    ),
                    lpar=[],
                    rpar=[],
                ),
                args=[
                    cst.Arg(
                        value=cst.SimpleString(
                            value="'utf-8'",
                            lpar=[],
                            rpar=[],
                        ),
                        keyword=None,
                        equal=cst.MaybeSentinel.DEFAULT,
                        comma=cst.MaybeSentinel.DEFAULT,
                        star='',
                        whitespace_after_star=cst.SimpleWhitespace(
                            value='',
                        ),
                        whitespace_after_arg=cst.SimpleWhitespace(
                            value='',
                        ),
                    ),
                ],
                lpar=[],
                rpar=[],
            )
            return new_node
        else:
            return updated_node