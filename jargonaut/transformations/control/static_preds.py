import libcst as cst 
# from predicates import mba_preds
from jargonaut.transformations.control.pred_utils import generate_static_mba_equality_pred
from libcst.metadata import ParentNodeProvider, TypeInferenceProvider, PositionProvider
from libcst.metadata import ScopeProvider
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin


class InsertStaticOpaqueMBAPredicates(cst.CSTTransformer):
    """
    Inserts static opaque predicates into funtion bodies
    Toy example for now
    """
    def __init__(self, n_terms_range=[4, 6], inference=False):
        self.n_terms_range = n_terms_range
        self.inference = inference
        self.first_visit = True
        self.progress_msg = "Inserting static opaque predicates..."
        if inference is False:
            InsertStaticOpaqueMBAPredicates.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                PositionProvider,
                ScopeProvider,
            )
        else:
            InsertStaticOpaqueMBAPredicates.METADATA_DEPENDENCIES = (
                ParentNodeProvider,
                TypeInferenceProvider,
                PositionProvider,
                ScopeProvider
            )
    
    def visit_FunctionDef(self, node):
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(Spinners.pipe, text=self.progress_msg, timer=True)
            self.spinner.start()
            self.first_visit = False
        return True

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef):
        if original_node.name.value != "__init__":
            mba_pred = generate_static_mba_equality_pred()
            func_body = original_node.body
            body = func_body.body
            if_block = cst.If(
                test=mba_pred,
                body=cst.IndentedBlock(body),
                orelse=None
            )
            return updated_node.with_changes(
                body=cst.IndentedBlock(body=[if_block])
            )
        return original_node
        
