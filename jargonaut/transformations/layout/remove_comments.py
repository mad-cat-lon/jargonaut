import libcst as cst
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin


class RemoveComments(cst.CSTTransformer):
    """
    Removes comments from source code.
    """

    def __init__(self):
        self.first_visit = True
        self.progress_msg = "Removing comments..."
        self.spinner = None 
        
    def visit_Comment(self, node: cst.Comment):
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(
                Spinners.simpleDotsScrolling,
                text=self.progress_msg,
                timer=True
            )
            self.first_visit = False       

    def leave_Comment(
        self,
        original_node: cst.Comment,
        updated_node: cst.Comment
    ) -> cst.RemovalSentinel:
        return cst.RemoveFromParent()