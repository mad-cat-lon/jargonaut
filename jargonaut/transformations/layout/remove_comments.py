import libcst as cst


class RemoveComments(cst.CSTTransformer):
    """
    Removes comments from source code.
    """

    def __init__(self):
        self.first_visit = True
        self.progress_msg = "[-] Removing comments..."

    def leave_Comment(
        self,
        original_node: cst.Comment,
        updated_node: cst.Comment
    ) -> cst.RemovalSentinel:
        if self.first_visit is True:
            print(self.progress_msg)
            self.first_visit = False
        return cst.RemoveFromParent()