import libcst as cst
import random
from libcst.metadata import QualifiedNameProvider, QualifiedNameSource
from libcst.metadata import ScopeProvider, ClassScope
from libcst.metadata import ParentNodeProvider
from libcst.metadata import TypeInferenceProvider
from yaspin.spinners import Spinners
from yaspin import kbi_safe_yaspin


class SeedParams(cst.CSTTransformer):
    """
    Inserts random integer variables (with type hints for pyre) into 
    function arguments, changing all calls to those functions with the bogus
    values as well.
    """
    METADATA_DEPENDENCIES = (
        ParentNodeProvider,
        QualifiedNameProvider, 
        ScopeProvider,
        TypeInferenceProvider
    )

    def __init__(self):
        self.funcs = []
        self.num_params = 2
        self.first_visit = True
        self.progress_msg = "Seeding function definitions with bogus parameters..."
        self.spinner = None
        
    def visit_FunctionDef(self, node: cst.FunctionDef):
        if self.first_visit is True:
            self.spinner = kbi_safe_yaspin(
                Spinners.dots12,
                text=self.progress_msg,
                timer=True
            )
            # self.spinner.start()
            self.first_visit = False
        qualified_name = list(self.get_metadata(QualifiedNameProvider, node))
        scope = self.get_metadata(ScopeProvider, node)
        # NOTE: Don't touch class methods for now - we will deal with this along 
        # with RandomizeNames() once I figure out a robust solution
        if len(qualified_name) != 0 and not isinstance(scope, ClassScope):
            qualified_name = qualified_name[0]
            if qualified_name.source == QualifiedNameSource.LOCAL:
                if qualified_name.name not in self.funcs:
                    self.funcs.append(qualified_name.name)
        return True

    def leave_FunctionDef(
        self,
        original_node: cst.FunctionDef,
        updated_node: cst.FunctionDef
    ):
        qualified_name = list(self.get_metadata(QualifiedNameProvider, original_node))
        if len(qualified_name) != 0:
            qualified_name = qualified_name[0]
            if qualified_name.name in self.funcs:
                # Add bogus int params with annotations for pyre 
                new_params = list(original_node.params.params)
                for _ in range(self.num_params):
                    new_params.append(
                        cst.Param(
                            name=cst.Name(
                                value=''.join(
                                    random.choice("abcdefghijk") for _ in range(10)
                                ),
                            ),
                            annotation=cst.Annotation(
                                annotation=cst.Name(
                                    value="int"
                                )
                            )
                        )
                    )
                params = cst.Parameters(
                    params=tuple(new_params),
                    star_arg=original_node.params.star_arg,
                    kwonly_params=original_node.params.kwonly_params,
                    star_kwarg=original_node.params.star_kwarg,
                    posonly_params=original_node.params.posonly_params,
                    posonly_ind=original_node.params.posonly_ind
                )
                # print(original_node.params) 
                # print(params)
                return updated_node.with_changes(
                    params=params
                )
        return original_node
        
    def leave_Call(
        self,
        original_node: cst.Call,
        updated_node: cst.Call
    ):
        qualified_name = list(self.get_metadata(QualifiedNameProvider, original_node.func))
        # inferred_type = self.get_metadata(TypeInferenceProvider, original_node)
        # print(original_node)
        # print(f"[CALL] -> {inferred_type}")
        # print(qualified_name)
        if len(qualified_name) != 0:
            qualified_name = qualified_name[0]
            if qualified_name.name in self.funcs:
                new_args = list(original_node.args)
                for _ in range(self.num_params):
                    new_args.append(
                        cst.Arg(
                            value=cst.Integer(
                                value=str(random.randint(0, 100))
                            )
                        )
                    )
                return updated_node.with_changes(
                    args=tuple(new_args)
                )
        return updated_node