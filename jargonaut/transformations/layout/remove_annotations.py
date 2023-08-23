import libcst as cst
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin


class RemoveAnnotations(cst.CSTTransformer):
    def __init__(self):
        self.first_visit = True
        self.progress_msg = "Removing all annotations..."
        self.spinner = None 
    
    def visit_AnnAssign(
        self,
        node: cst.AnnAssign
    ):
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(
                Spinners.simpleDotsScrolling,
                text=self.progress_msg,
                timer=True
            )
            self.spinner.start()
            self.first_visit = False
        # Don't visit the child Annotation() if we already have an AnnAssign(),
        # since we are replacing it with Assign() 
        return False
    
    def leave_AnnAssign(
        self,
        original_node: cst.AnnAssign,
        updated_node: cst.AnnAssign
    ) -> cst.Assign:
        return cst.Assign(
            targets=[
                cst.AssignTarget(
                    target=cst.Name(
                        value=updated_node.target.value
                    )
                )
            ],
            value=updated_node.value
        )
    
    def leave_Annotation(
        self,
        original_node: cst.Annotation,
        updated_node: cst.Annotation
    ) -> cst.RemovalSentinel:
        return cst.RemoveFromParent()