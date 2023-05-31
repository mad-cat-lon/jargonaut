import libcst as cst
import random 
from libcst.metadata import ParentNodeProvider, TypeInferenceProvider, PositionProvider
from libcst.metadata import ScopeProvider
from .mba_utils import constant_to_mba


class ConstIntToLinearMBA(cst.CSTTransformer):
    """
    Transforms constants to MBA expressions
    Can specify whether you want to use affine or polynomial functions (todo)
    
    Attributes:
        n_term_range: range for the number of terms in the MBA expression
        inference:  Use type inference
    """

    def __init__(
        self,
        n_terms_range=[4, 6],
        inference=False
    ):
        self.n_terms_range = n_terms_range
        self.inference = inference
        self.first_visit = True
        self.progress_msg = "[-] Transforming integer constants to linear MBA forms..."
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
    
    def leave_Integer(
            self,
            original_node: cst.Integer,
            updated_node: cst.Integer
    ):
        if self.first_visit:
            print(self.progress_msg)
            self.first_visit = False
        if self.inference:
            constant_mba = constant_to_mba(
                original_node.evaluated_value,
                n_terms=random.choice(self.n_terms_range),
                as_obj=False
            )
            scope = self.get_metadata(ScopeProvider, original_node)
            # Let's check if there are any integer variables in the scope we can use for confusion
            assignments_in_scope = []
            for assign in scope.assignments:
                # Only take Name() for now
                if isinstance(assign.node, cst.Name):
                    # Check if it's in scope
                    if assign.node.value in scope:
                        node_pos = self.get_metadata(PositionProvider, original_node).start 
                        assign_pos = self.get_metadata(PositionProvider, assign.node).start
                        # HACK: Don't use the assignment unless it appears before our current node
                        if node_pos.line > assign_pos.line:
                            assignments_in_scope.append(assign.node)
            # Do type inferencing here to find Name() nodes that are of type int
            int_names = []
            for node in assignments_in_scope:
                # HACK: When we run PatchReturns() before this transformation,
                # we insert a Name(value="frame") to do the patching
                # Pyre doesn't know about this yet so we need to handle the KeyError
                try:
                    inferred_type = self.get_metadata(TypeInferenceProvider, node)
                    if inferred_type == "int":
                        int_names.append(node)
                except KeyError:
                    pass 
            if int_names:
                # Replace x and y in the constant_mba expression
                x = random.choice(int_names)
                y = random.choice(int_names)
                constant_mba = constant_mba.replace("x", x.value)
                constant_mba = constant_mba.replace("y", y.value)
                return cst.parse_expression(constant_mba)
            else:
                # print("No names found, inserting statements")
                # We have a few options here
                # 1. Just use random integers for x and y
                # 2. Define integer vars before the expression 
                # 3. If inside a function, add parameters and edit all calls to include vars
                # HACK: Doing option 1 for now: inserting statements before a node is finicky 
                # x_name = ''.join([random.choice("abcdefghihklmnopqrstuv") for _ in range(10)])
                # y_name = ''.join([random.choice("abcdefghihklmnopqrstuv") for _ in range(10)])
                x_val = random.randint(0, 1000)
                y_val = random.randint(0, 1000)
                constant_mba = constant_mba.replace("x", str(x_val))
                constant_mba = constant_mba.replace("y", str(y_val))
                return cst.parse_expression(constant_mba)
        else:
            constant_mba = constant_to_mba(
                int(original_node.evaluated_value),
                as_obj=False
            )
            x_val = random.randint(0, 1000)
            y_val = random.randint(0, 1000)
            constant_mba = constant_mba.replace("x", str(x_val))
            constant_mba = constant_mba.replace("y", str(y_val))
            return cst.parse_expression(constant_mba)