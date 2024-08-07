from libcst._nodes.statement import FunctionDef
from libcst.metadata import ScopeProvider
import libcst as cst
import random
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin
import sys

class PatchReturns(cst.CSTTransformer):
    """
    Does runtime bytecode patching to obscure the real return value of functions
    Example:
        def my_func(x):
            def patch_bytecode(y):
                ....
            patch_bytecode("Will actually be returned")
            return "Won't be returned"
    WARNING: this transformation breaks Nuitka! 
    https://nuitka.net/doc/user-manual.html#the-co-code-attribute-of-code-objects
    """
    # TODO: Do insertion of import inspect, from ctypes import memmove
    METADATA_DEPENDENCIES = (ScopeProvider,)

    def __init__(self, avoid=None):
        if sys.version_info.minor > 10:
            print("[!] PatchReturns() cannot be used for Python >3.10 due to PEP 659.")
        self.avoid = avoid
        self.first_visit = True
        self.progress_msg = "Patching function return values..."
        self.spinner = None 

    def visit_FunctionDef(self, node):
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(Spinners.pipe, text=self.progress_msg, timer=True)
            self.spinner.start()
            self.first_visit = False
        return True

    def leave_FunctionDef(self, original_node: FunctionDef, updated_node: FunctionDef) -> None:
        # Go inside indented block (body=IndentedBlock)
        patched_body = list(original_node.body.body)
        ret_idx = []
        for i, x in enumerate(patched_body):
            if isinstance(x, cst.SimpleStatementLine):
                if len(x.body) == 1 and isinstance(x.body[0], cst.Return):
                    # Only match functions with one return statement (no if blocks)
                    # Learn how matching works so we can do this to all funcs
                    # I know this is bad code! Just want to get this working 
                    ret_idx.append(i)
        for idx in ret_idx:
            func_name = "_" + ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
            arg_name = ''.join(random.choices("abcdefhjiklmnopqrstuvwxyz", k=4))
            func = f"""def {func_name}({arg_name}):
    frame = inspect.currentframe().f_back
    code = frame.f_code.co_code
    pos = frame.f_lasti
    buffer = bytes(code)
    memmove(id(buffer)+0x20 + pos + 2, b"\\x53\\x00", 2)
    return {arg_name}"""
            func = cst.parse_statement(func)
            # Insert the func definition      
            patched_body.insert(idx, func)
            # Insert call to the func we made before the original ret statement
            old_ret_val = patched_body[idx + 1].body[0].value
            patched_body.insert(
                idx + 1,
                cst.SimpleStatementLine(
                    body=[
                        cst.Expr(
                            value=cst.Call(
                                func=cst.Name(
                                    value=func_name
                                ), 
                                args=[
                                    cst.Arg(
                                        value=old_ret_val
                                    ),
                                ]
                            )
                        )
                    ]
                )
            )
            # Replace the original ret statement's value with something else
            # Just a string literal for now - in the future we could make this return random
            # variables in the parent function's scope, etc. for maximum confusion
            patched_body[idx + 2] = cst.SimpleStatementLine(
                body=[
                    cst.Return(
                        value=cst.SimpleString(
                            value='"LOLOLOLOL"'
                        )
                    )
                ]
            )
        patched_body = tuple(patched_body)
        func_body = cst.IndentedBlock(body=patched_body)
        return updated_node.with_changes(
            body=func_body
        )
    