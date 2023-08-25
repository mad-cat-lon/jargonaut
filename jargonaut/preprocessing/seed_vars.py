import libcst as cst
import random
from libcst.metadata import QualifiedNameProvider
from libcst.metadata import ScopeProvider
from libcst.metadata import ParentNodeProvider
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin


class SeedVars(cst.CSTTransformer):
    """
    Inserts random integer variables
    """
    METADATA_DEPENDENCIES = (
        ParentNodeProvider,
        QualifiedNameProvider, 
        ScopeProvider
    )

    def __init__(self):
        self.max_vars = 15
        self.first_visit = True
        self.progress_msg = "Seeding random integer variables..."
        self.spinner = None

    def on_visit(self, node):
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(
                Spinners.dots12,
                text=self.progress_msg,
                timer=True
            )
            self.spinner.start()
            self.first_visit = False
        return True 
    
    def generate_random_assignment(self, type=None):
        """
        Generate random integer variable and assigns random value
        We have multiple types:
        Default:
            x: int = 1000
        """
        name = f"seed_int_var_{''.join(random.choices('abcdef', k=10))}"
        if type is None:
            val = random.randint(0, 10000)
            assign = cst.SimpleStatementLine(
                body=[
                    cst.AnnAssign(
                        target=cst.Name(
                            value=name
                        ),
                        annotation=cst.Annotation(
                            annotation=cst.Name(
                                value='int'
                            )
                        ),
                        value=cst.Integer(
                            value=str(val)
                        ),
                        equal=cst.AssignEqual(
                            whitespace_before=cst.SimpleWhitespace(
                                value=' ',
                            ),
                            whitespace_after=cst.SimpleWhitespace(
                                value=' ',
                            )
                        ),
                        semicolon=cst.MaybeSentinel.DEFAULT
                    )
                ]
            )
        return assign

    def leave_FunctionDef(
        self,
        original_node: cst.FunctionDef,
        updated_node: cst.FunctionDef
    ):
        patched_body = list(updated_node.body.body)
        # Generate assignments and insert them randomly
        assigns = [
            self.generate_random_assignment() for _ in range(
                random.randint(1, self.max_vars)
            )
        ]
        body_len = len(patched_body)
        # insert them! 
        for assign in assigns:
            patched_body.insert(random.randint(0, body_len), assign)         
        return updated_node.with_changes(
            body=cst.IndentedBlock(body=tuple(patched_body))
        )
    
    def leave_Module(
        self,
        original_node: cst.Module,
        updated_node: cst.Module
    ):
        patched_body = list(updated_node.body)
        # Generate assignments and insert them randomly
        assigns = [
            self.generate_random_assignment() for _ in range(
                random.randint(1, self.max_vars)
            )
        ]
        # insert them! 
        body_len = len(patched_body)
        for assign in assigns:
            patched_body.insert(random.randint(0, body_len), assign)
        return updated_node.with_changes(body=tuple(patched_body))