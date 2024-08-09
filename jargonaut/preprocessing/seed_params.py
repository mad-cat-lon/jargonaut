import libcst as cst
from libcst.metadata import ParentNodeProvider, QualifiedNameProvider
from libcst.metadata import ScopeProvider, ClassScope
from yaspin import kbi_safe_yaspin
from yaspin.spinners import Spinners
import random


class SeedParams(cst.CSTTransformer):
    """
    SeedParams class extends the CSTTransformer from libcst to insert random integer variables
    (with type hints for pyre) into function arguments. This also updates all calls to the funcs
    with the new random variables.
    """

    METADATA_DEPENDENCIES = (ParentNodeProvider, QualifiedNameProvider, ScopeProvider)

    def __init__(self):
        """
        Initialize SeedParams object.
        """
        # Set of function names
        self.funcs = set()
        # Number of random parameters to add
        self.num_params = 8
        # Flag to indicate first visit
        self.first_visit = True
        # Progress message for spinner
        self.progress_msg = "Seeding function definitions with bogus parameters..."
        # Spinner for indicating progress
        self.spinner = None

    def visit_FunctionDef(self, node: cst.FunctionDef):
        """
        Visit each Function Definition in the code and collect its qualified name.
        Initialize spinner on the first visit.
        
        Args:
            node (cst.FunctionDef): Function definition node.
            
        Returns:
            bool: Always returns True to continue traversal.
        """
        if self.first_visit:
            self.spinner = kbi_safe_yaspin(
                Spinners.dots12,
                text=self.progress_msg,
                timer=True
            )
            self.spinner.start()
            self.first_visit = False

        # Get metadata for the current function definition
        qualified_names = self.get_metadata(QualifiedNameProvider, node)
        scope = self.get_metadata(ScopeProvider, node)

        # Add function name to the set if it's not a class method
        if qualified_names and not isinstance(scope, ClassScope):
            qualified_name = next(iter(qualified_names)).name
            self.funcs.add(qualified_name)

        return True

    def leave_FunctionDef(
        self, 
        original_node: cst.FunctionDef,
        updated_node: cst.FunctionDef
    ):
        """
        Modify the function definition to include new random integer parameters.
        
        Args:
            original_node (cst.FunctionDef): Original function definition node.
            updated_node (cst.FunctionDef): Updated function definition node.
            
        Returns:
            cst.FunctionDef: Modified function definition node.
        """
        qualified_names = self.get_metadata(QualifiedNameProvider, original_node)
        
        if qualified_names:
            qualified_name = next(iter(qualified_names)).name
            if qualified_name in self.funcs:
                updated_params = list(original_node.params.params)
                new_params = [
                    cst.Param(
                        name=cst.Name(
                            value=f"seed_int_param_{''.join(random.choices('abcdef', k=10))}"
                        ),
                        annotation=cst.Annotation(annotation=cst.Name(value="int"))
                    ) for _ in range(self.num_params)
                ]
                # Find the location of the first default and insert before it
                insert_idx = -1
                for i, p in enumerate(original_node.params.params):
                    if isinstance(p.equal, cst.AssignEqual):
                        insert_idx = i
                        break
                if insert_idx != -1:
                    updated_params = (
                        updated_params[:insert_idx] +
                        new_params +
                        updated_params[insert_idx:]
                    )
                else:
                    updated_params = updated_params + new_params
                return updated_node.with_changes(
                    params=original_node.params.with_changes(params=tuple(updated_params))
                )

        return original_node

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call):
        """
        Modify the function calls to include new random int arguments for the modified functions.
        
        Args:
            original_node (cst.Call): Original function call node.
            updated_node (cst.Call): Updated function call node.
            
        Returns:
            cst.Call: Modified function call node.
        """
        qualified_names = self.get_metadata(QualifiedNameProvider, original_node.func)

        if qualified_names:
            qualified_name = next(iter(qualified_names)).name
            if qualified_name in self.funcs:
                updated_args = list(original_node.args)
                new_args = [
                    cst.Arg(
                        value=cst.Integer(
                            value=str(random.randint(0, 1000))
                        )
                    ) for _ in range(self.num_params)
                ]
                # Find the location of the first default and insert before it
                insert_idx = -1
                for i, a in enumerate(original_node.args):
                    if isinstance(a.equal, cst.AssignEqual):
                        insert_idx = i
                        break
                if insert_idx != -1:
                    updated_args = (
                        updated_args[:insert_idx] +
                        new_args +
                        updated_args[insert_idx:]
                    )
                else:
                    updated_args = updated_args + new_args
                return updated_node.with_changes(
                    args=tuple(updated_args)
                )
        return updated_node
