import libcst as cst
import random 
from libcst.metadata import ParentNodeProvider, TypeInferenceProvider, PositionProvider
from libcst.metadata import ScopeProvider
from .mba_utils import constant_to_mba
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin


class ConstIntToLinearMBA(cst.CSTTransformer):
    """
    Transforms constants to MBA expressions
    Can specify whether you want to use affine or polynomial functions (todo)
    
    Attributes:
        n_term_range: range for the number of terms in the MBA expression
        inference:  Use type inference
    """

    def __init__(self, n_terms_range=[4, 6], inference=False):
        self.n_terms_range = n_terms_range
        self.inference = inference
        self.first_visit = True
        self.progress_msg = "Transforming all integer constants to linear MBA forms..."
        if inference is False:
            ConstIntToLinearMBA.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                PositionProvider,
                ScopeProvider,
            )
        else:
            ConstIntToLinearMBA.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                TypeInferenceProvider,
                PositionProvider,
                ScopeProvider
            )
        self.curr_scope = (None, [])
        self.int_names_available = False
        self.spinner = None

    def get_int_names_in_scope(self, node, scope):
        # HACK: We get the assignments in the scope that are of type() and appear before the
        # target node in the source file
        assigns_in_scope = [
            assign.node for assign in scope.assignments if isinstance(assign.node, cst.Name)
            and (
                ((self.get_metadata(PositionProvider, node).start).line) >
                ((self.get_metadata(PositionProvider, assign.node).start).line)
            )
        ]
        # print(assigns_in_scope)
        """        
        for assign in scope.assignments:
            # Only take Name() for now
            if isinstance(assign.node, cst.Name):
                # Check if it's in scope
                node_pos = self.get_metadata(PositionProvider, node).start 
                assign_pos = self.get_metadata(PositionProvider, assign.node).start
                # HACK: Don't use the assignment unless it appears before our current node
                if node_pos.line > assign_pos.line:
                    assigns_in_scope.append(assign.node)
        """
        # Do type inferencing here to find Name() nodes that are of type int
        int_names = []
        for node in assigns_in_scope:
            # HACK: When we run PatchReturns() before this transformation,
            # we insert a Name(value="frame") to do the patching
            # Pyre doesn't know about this yet so we need to handle the KeyError
            try:
                inferred_type = self.get_metadata(TypeInferenceProvider, node)
                if inferred_type == "int":
                    int_names.append(node)
            except KeyError:
                pass
        return int_names 

    def visit_Integer(self, node: cst.Integer):
        if self.first_visit:
            self.spinner = kbi_safe_yaspin(Spinners.dots12, text=self.progress_msg, timer=True)
            self.spinner.start()
            self.first_visit = False
        scope = self.get_metadata(ScopeProvider, node)
        if self.curr_scope[0] != scope:
            # print("Entering new scope")
            # print(f"Old scope: {self.curr_scope}")
            # print(f"New scope {scope} at {cst.parse_module('').code_for_node(node)}")
            int_names_in_scope = self.get_int_names_in_scope(node, scope)
            # print(int_names_in_scope)
            self.curr_scope = (scope, int_names_in_scope)
            if len(int_names_in_scope) == 0:
                self.int_names_available = False
        else:
            if len(self.curr_scope[1]) == 0:
                self.int_names_available = False
            else:
                self.int_names_available = True
        return True 
        
    def leave_Integer(
        self,
        original_node: cst.Integer,
        updated_node: cst.Integer
    ):
        constant_mba = constant_to_mba(
            int(original_node.evaluated_value),
            n_terms=random.choice(self.n_terms_range),
            as_obj=False
        )
        if self.int_names_available:
            # Replace x and y with variables in the current scope 
            # TODO: Optimize performance
            if self.inference:
                int_names = self.curr_scope[1]
                # Replace x and y in the constant_mba expression
                x = random.choice(int_names)
                y = random.choice(int_names)
                constant_mba = constant_mba.replace("x", x.value)
                constant_mba = constant_mba.replace("y", y.value)
                return cst.parse_expression(constant_mba)
        else:
            x_val = random.randint(0, 1000)
            y_val = random.randint(0, 1000)
            constant_mba = constant_mba.replace("x", str(x_val))
            constant_mba = constant_mba.replace("y", str(y_val))
            return cst.parse_expression(constant_mba)
