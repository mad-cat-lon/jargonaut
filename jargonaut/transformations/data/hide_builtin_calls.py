import libcst as cst
import random 


class HideBuiltinCalls(cst.CSTTransformer):
    """
    Replaces calls to built-in functions, eg.
    print("abcd") ->
    getattr(
        __builtins__,
        BrokenPipeError.__name__[8]+round.__name__[0]+...
    )
    """

    def __init__(self):
        self.first_visit = True 
        self.progress_msg = "[-] Obfuscating calls to builtin functions..."
        self.builtin_names = [
            name for name, obj in 
            __builtins__.items()
        ]

    def hide_call(self, func_name):
        # We do getattr(__builtins__, "builtin_func_name")(args) and construct
        # the string out of other builtin names 
        # There are probably other more obscure tricks you can do, but this will suffice
        # WARNING: string concatenation counts as a BinaryOperation, so don't apply this
        # before LinearMBA unless you want to waste a lot of time and energy.
        # https://lwn.net/Articles/551426/
        result = []
        builtins_dict = __builtins__

        # Handling edge cases
        if "__loader__" in builtins_dict.keys():
            del builtins_dict["__loader__"]
        if "__doc__" in builtins_dict.keys():
            del builtins_dict["__doc__"]
        if "__spec__" in builtins_dict.keys():
            del builtins_dict["__spec__"]

        # Quick hack to retry in case we generated it wrong
        # TODO: Fix root issue with how hasattr() is being used
        while True:
            stack = [c for c in func_name]
            result = []
            while len(stack) > 0:
                builtins_shuffled = list(builtins_dict)
                random.shuffle(builtins_shuffled)
                builtins_shuffled = {key: builtins_dict[key] for key in builtins_shuffled}
                for name, obj in builtins_shuffled.items():
                    if hasattr(obj, "__name__"):
                        if name != func_name and (obj.__name__).find(stack[0]) != -1:
                            result.append(
                                f"{name}.__name__[{(obj.__name__).find(stack[0])}]"
                            )
                            stack.pop(0)
                            break
                    elif hasattr(obj, "__class__"):
                        if hasattr(obj.__class__, "__name__"):
                            if name != func_name and (obj.__class__.__name__).find(stack[0]) != -1:
                                classname = obj.__class__.__name__
                                result.append(
                                    f"{name}.__class__.__name__[{classname.find(stack[0])}]"
                                )
                                stack.pop(0)
                                break
            result = "+".join(result)
            if len(stack) == 0 and eval(result) == func_name:
                return result
            else:
                pass 
            # TODO: Add more confusion 
            # For example, instead of doing list.__class__.__name__ we can do something like:
            # [1, 3, 43, 5, 6, "\x00", "\xef"].__class__.__name__
            # Or even better, we can find names of the same type in the current scope and 
            # construct our builtin call from those

    def leave_Call(
        self,
        original_node: cst.Call,
        updated_node: cst.Call
    ):
        if self.first_visit is True:
            print(self.progress_msg)
            self.first_visit = False
        if isinstance(original_node.func, cst.Name):
            if original_node.func.value in self.builtin_names:
                obfus_func_str = self.hide_call(original_node.func.value)
                final_call = cst.Call(
                    cst.Call(
                        func=cst.Name(
                            value="getattr"
                        ),
                        args=[
                            cst.Arg(
                                value=cst.Name(
                                    value="__builtins__"
                                ),
                                keyword=None
                            ),
                            cst.Arg(
                                value=cst.parse_expression(obfus_func_str),
                                keyword=None
                            )
                        ]
                    ),
                    args=original_node.args
                )
                return final_call
        return original_node