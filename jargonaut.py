from jargonaut.transformations import data, layout, control
import libcst as cst
from libcst.metadata import FullRepoManager, TypeInferenceProvider
import argparse 
import platform


def main():
    prog = "jargonaut"
    description = "jargonaut - reliable and configurable Python to Python obfuscation"
    parser = argparse.ArgumentParser(
        prog=prog,
        description=description
    )
    parser.add_argument(
        "-in_file",
        help="path to target file",
    )
    parser.add_argument(
        "-out_file",
        help="path to obfuscated file",
    )
    parser.add_argument(
        "--inference",
        default=False,
        dest="inference",
        help="use pyre's type inference. Linux/WSL only.",
        action="store_true"
    )
    args = parser.parse_args()
    do_inference = args.inference
    if do_inference is False:
        print("[!] Type inference is not enabled. Obfuscated code may not be reliable.")
    else:
        system = platform.system()
        if system == "Windows":
            print("[!] Pyre is not currently supported on Windows.")
    with open(args.in_file, "r", encoding="utf-8") as in_file:
        tree = cst.parse_module(in_file.read())
        transformations = [
            # Patch function return values
            control.PatchReturns(),
            # Replace integer literals and binay operations with linear MBAs
            # You can set the recursion depth up to 30 if desired
            data.LinearMBA(
                sub_expr_depth=[1, 3],
                super_expr_depth=[3, 7],
                inference=do_inference
            ),
            # Replace string literals with lambda functions
            data.LambdaString(),
            # Obfuscate builtin calls
            data.HideBuiltinCalls(),
            # Randomize names
            layout.RandomizeNames(),
            # Remove comments
            layout.RemoveComments()
        ]
        for i, t in enumerate(transformations):
            if do_inference is True:
                manager = FullRepoManager(
                    ".",
                    {args.in_file},
                    {TypeInferenceProvider}
                )
                wrapper = cst.MetadataWrapper(tree, cache=manager.get_cache_for_path(args.in_file))
                # wrapper = manager.get_metadata_wrapper_for_path(args.in_file)
                tree = wrapper.visit(t)
            else:
                wrapper = cst.MetadataWrapper(tree)
                tree = wrapper.visit(t)
        obfus = tree.code
        with open(args.out_file, "w", encoding="utf-8") as out_file:
            # Most specify encoding in output file due to binary string obfuscation
            out_file.write("# -*- coding: utf-8 -*\n")
            # For PatchReturn(): this is temporary
            out_file.write("import inspect\n")
            out_file.write("from ctypes import memmove\n")
            out_file.write(obfus)
        print("[-] Done.")


if __name__ == "__main__":
    main()