import libcst as cst 
from math import ceil, log
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin
import re


class StringToLambdaExpr(cst.CSTTransformer):
    """
    Obfuscates string literals by converting them to an extremely
    opaque lambda expression
    """
    #BUG: doesn't deal with escape characters properly
    def __init__(self, avoid=None):
        self.avoid = avoid
        self.first_visit = True 
        self.progress_msg = "Obfuscating string literals with lambda expressions..."
        self.spinner = None 
        
    def encode(self, num, depth):
        if num == 0:
            return "_ - _"
        if num <= 8:
            return "_" * num
        return "(" + self.convert(num, depth + 1) + ")"

    def convert(self, num, depth=0):
        result = ""
        while num:
            base = shift = 0
            diff = num
            span = int(ceil(log(abs(num), 1.5))) + (16 >> depth)
            for test_base in range(span):
                for test_shift in range(span):
                    test_diff = abs(num) - (test_base << test_shift)
                    if abs(test_diff) < abs(diff):
                        diff = test_diff
                        base = test_base
                        shift = test_shift
            if result:
                result += " + " if num > 0 else " - "
            elif num < 0:
                base = -base
            if shift == 0:
                result += self.encode(base, depth)
            else:
                result += "(%s << %s)" % (self.encode(base, depth), self.encode(shift, depth))
            num = diff if num > 0 else -diff
        return result

    def visit_Call(self, node: cst.Call):
        # This implementation breaks open(filename, mode) so we avoid it 
        if isinstance(node.func, cst.Name):
            if node.func.value == "open":
                return False 

    def visit_SimpleString(self, node: cst.SimpleString):
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(Spinners.dots12, text=self.progress_msg, timer=True)
            self.spinner.start()
            self.first_visit = False  
        return True
    
    def leave_SimpleString(
        self,
        original_node: cst.SimpleString,
        updated_node: cst.SimpleString
    ):
        # Only convert strings of len > 3 and don't convert strings with prefixes
        # Also avoid escape characters
        if (
            len(original_node.value) > 3 
            and not original_node.prefix 
            and not re.findall(r'\\.', original_node.value)
        ):
            codes = [ord(c) for c in original_node.value]
            num = sum(codes[i] * 256 ** i for i in range(len(codes)))
            obfus = self.convert(num)
            # Source: https://benkurtovic.com/2014/06/01/obfuscating-hello-world.html
            decode_func = f"(lambda _, __, ___, ____, _____, ______, _______, ________:\
    (lambda _, __, ___: _(_, __, ___))(\
            lambda _, __, ___:\
                bytes([___ % __]) + _(_, __, ___ // __) if ___ else\
                (lambda: _).__code__.co_lnotab,\
            _ << ________,\
            {obfus}\
        )\
    )(\
        *(lambda _, __, ___: _(_, __, ___))(\
            (lambda _, __, ___:\
                [__(___[(lambda: _).__code__.co_nlocals])] +\
                _(_, __, ___[(lambda _: _).__code__.co_nlocals:]) if ___ else []\
            ),\
            lambda _: _.__code__.co_argcount,\
            (\
                lambda _: _,\
                lambda _, __: _,\
                lambda _, __, ___: _,\
                lambda _, __, ___, ____: _,\
                lambda _, __, ___, ____, _____: _,\
                lambda _, __, ___, ____, _____, ______: _,\
                lambda _, __, ___, ____, _____, ______, _______: _,\
                lambda _, __, ___, ____, _____, ______, _______, ________: _\
            )\
        )\
    ).decode(\"utf-8\")[1:-1]"
            result = cst.parse_expression(decode_func)
            return result
        return original_node