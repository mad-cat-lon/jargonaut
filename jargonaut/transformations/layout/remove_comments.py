import libcst as cst


class RemoveComments(cst.CSTTransformer):
    """
    Removes comments from source code.
    """

    def leave_Comment(
        self,
        original_node: cst.Comment,
        updated_node: cst.Comment
    ) -> cst.RemovalSentinel:
        return cst.RemoveFromParent()