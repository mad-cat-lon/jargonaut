import libcst as cst
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin


class RemoveAnnotations(cst.CSTTransformer):
    def __init__(self):
        self.first_visit = True
        self.progress_msg = "Removing all annotations..."
        self.spinner = None 
    
    def visit_Annotation(self, node):
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(
                Spinners.simpleDotsScrolling,
                text=self.progress_msg,
                timer=True
            )
            self.spinner.start()
            self.first_visit = False
        return True 
    
    def leave_Annotation(
        self,
        original_node: cst.Annotation,
        updated_node: cst.Annotation
    ) -> cst.RemovalSentinel:
        return cst.RemoveFromParent()