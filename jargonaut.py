from jargonaut.transformations import data, layout, control
import libcst as cst
from libcst.metadata import FullRepoManager, TypeInferenceProvider
from timeit import default_timer as timer
import argparse 
import platform
import os


def handle_args():
    prog = "jargonaut"
    description = "jargonaut - reliable and configurable Python to Python obfuscation"
    parser = argparse.ArgumentParser(
        prog=prog,
        description=description
    )
    parser.add_argument(
        "-in_file",
        help="Path to target file",
    )
    parser.add_argument(
        "-out_file",
        help="Path to obfuscated file",
    )
    parser.add_argument(
        "--inference",
        default=False,
        dest="inference",
        help="Use pyre for type inferencing for more stable code generation. Linux/WSL only.",
        action="store_true"
    )
    parser.add_argument(
        "--print-stats",
        default=True,
        dest="print_stats",
        help="Print statistics after obfuscation",
        action="store_true"
    )
    args = parser.parse_args()
    return args


def print_stats(in_file, out_file, time):
    in_file_lc = 0
    out_file_lc = 0
    # Calculate line count changes
    with open(in_file, "r") as f:
        in_file_lc = len(f.readlines())
    with open(out_file, "r") as f:
        out_file_lc = len(f.readlines())
    print(f"[*] Operation completed in {time} seconds")
    print(f"[*] {in_file_lc} lines -> {out_file_lc} lines")
    # Calculate file size changes 
    in_file_size = os.stat(in_file).st_size
    out_file_size = os.stat(out_file).st_size
    print(f"[*] {in_file_size} bytes -> {out_file_size} bytes")


def main():
    args = handle_args()
    do_inference = args.inference
    if do_inference is False:
        print("[!] Type inferencing with pyre is not enabled. Obfuscated code may not be reliable.")
    else:
        system = platform.system()
        if system == "Windows":
            print("[!] Pyre is not currently supported on Windows.")
            exit()
        # os.system("pyre")
    start_time = timer()
    with open(args.in_file, "r", encoding="utf-8") as in_file:
        tree = cst.parse_module(in_file.read())
        transformations = [
            # Patch function return values
            control.PatchReturns(),
            # Transform expressions to linear MBAs
            # You can set the recursion depth up to 30, but the file 
            # may be 10-50x larger and obfuscation may take up to an hour
            data.ExprToLinearMBA(
                sub_expr_depth=[1, 3],
                super_expr_depth=[2, 4],
                inference=do_inference
            ),
            # Obfuscate builtin calls
            data.HideBuiltinCalls(),
            # Transform integers to linear MBAs
            data.ConstIntToLinearMBA(
                n_terms_range=[4, 6],
                inference=do_inference
            ),
            # Replace string literals with lambda functions
            data.StringToLambdaExpr(),
            # Randomize names
            layout.RandomizeNames(),
            # Remove comments
            layout.RemoveComments()
        ]
        for i, t in enumerate(transformations):
            if do_inference is True:
                manager = FullRepoManager(
                    os.path.dirname(args.in_file),
                    {args.in_file},
                    {TypeInferenceProvider}
                )
                wrapper = cst.MetadataWrapper(tree, cache=manager.get_cache_for_path(args.in_file))
                # wrapper = manager.get_metadata_wrapper_for_path(args.in_file)
                tree = wrapper.visit(t)
            else:
                wrapper = cst.MetadataWrapper(tree)
                tree = wrapper.visit(t)
            t.spinner.ok()
        obfus = tree.code
        with open(args.out_file, "w", encoding="utf-8") as out_file:
            # Most specify encoding in output file due to binary string obfuscation
            out_file.write("# -*- coding: utf-8 -*\n")
            # For PatchReturn(): this is temporary
            out_file.write("import inspect\n")
            out_file.write("from ctypes import memmove\n")
            out_file.write(obfus)
        print("[-] Done all transformations.")
        end_time = timer()
        if args.print_stats:
            print_stats(args.in_file, args.out_file, (end_time - start_time))


if __name__ == "__main__":
    main()