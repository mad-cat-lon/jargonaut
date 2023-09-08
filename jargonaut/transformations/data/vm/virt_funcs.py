import libcst as cst
from .compiler import Compiler
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin
from .vm import VirtualMachine
import inspect


class VirtualizeFuncs(cst.CSTTransformer):
    """
    Does source-to-source virtualization of target functions
    """
    def __init__(self, targets=[], inference=False):
        self.targets = targets
        self.inference = inference
        self.first_visit = True
        self.progress_msg = "Virtualizing functions..."
        self.spinner = None 
        self.compiler = Compiler()

    def visit_FunctionDef(self, node):
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(Spinners.dots12, text=self.progress_msg, timer=True)
            self.spinner.start()
            self.first_visit = False

    def leave_FunctionDef(
        self,
        original_node: cst.FunctionDef,
        updated_node: cst.FunctionDef
    ):
        if original_node.name.value in self.targets:
            entry = self.compiler.compile_func(original_node)
            entry_code = cst.parse_module(entry).body
            func_body = cst.IndentedBlock(entry_code)
            return updated_node.with_changes(
                body=func_body
            )
        return original_node
    
    def leave_Module(
        self,
        original_node: cst.Module,
        updated_node: cst.Module
    ):
        # Look for end of import statements 
        patched_body = list(updated_node.body)
        vm_source = inspect.getsource(VirtualMachine)
        vm_code= cst.parse_statement(vm_source)
        # HACK: find out proper location to insert 
        patched_body.insert(2, vm_code)
        
        return updated_node.with_changes(
            body=tuple(patched_body)
        )



