import libcst as cst
import dis
import random
from .mappings import OPCODE_MAP


class Compiler:
    """
    Compiles functions to obfuscated bytecode
    """
    
    def __init__(self):
        # self.vm = VirtualMachine()
        self.opname_map = {}

    def get_op(self, instr: dis.Instruction):
        return random.choice(OPCODE_MAP[instr.opname])

    def compile_func(self, func: cst.FunctionDef):   
        # Convert node into code representation
        code = cst.parse_module("").code_for_node(func)
        # Compile code
        code_obj = compile(code, "<string>", "exec")
        namespace = {}
        exec(code_obj, namespace)
        # Retrieve function from namespace 
        func = namespace[func.name.value]
        # print(f"names: {func.__code__.co_names}")
        # print(f"consts: {func.__code__.co_consts}")
        # print(f"varnames: {func.__code__.co_varnames}")
        # print(f"cellvars: {func.__code__.co_cellvars}")
        bytecode = []
        # print(dis.dis(func))
        for index, py_instr in enumerate(dis.get_instructions(func)):
            # print(py_instr)         
            jarg_instr = self.get_op(py_instr)
            self.opname_map[str(jarg_instr[1])] = py_instr.opname
            bytecode.append(jarg_instr[1])
            if py_instr.opcode in dis.hasjrel:
                bytecode.append(py_instr.arg)
            elif py_instr.opcode in dis.hasjabs:
                bytecode.append(py_instr.argval-2)
            elif (
                py_instr.opcode in dis.haslocal
                or py_instr.opcode in dis.hasconst
                or py_instr.opcode in dis.hasfree
                or py_instr.opcode in dis.hasname
                or py_instr.opcode in dis.hascompare
                or py_instr.arg is not None
            ):
                bytecode.append(py_instr.arg)
            else:
                bytecode.append(1337)
        # print(bytecode)
        final = f"""
opname_map = {self.opname_map}
names = {func.__code__.co_names}
consts = {func.__code__.co_consts}
varnames = {func.__code__.co_varnames}
cellvars = {func.__code__.co_cellvars}
bytecode = {bytecode}
vm = VirtualMachine(
    opname_map,
    globals(),
    locals(),
    names,
    consts,
    varnames,
    bytecode
)
out = vm.run()
return out
"""
        return final
        # return {
        #     "names":  func.__code__.co_names,
        #     "consts": func.__code__.co_consts,
        #     "varnames": func.__code__.co_varnames,
        #     "cellvars": func.__code__.co_cellvars,
        #     "bytecode": bytecode
        # }
        