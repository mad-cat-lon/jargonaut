from jargonaut.transformations import data, layout, control
from jargonaut import preprocessing
import libcst as cst
from libcst.metadata import FullRepoManager, TypeInferenceProvider
from timeit import default_timer as timer
import argparse 
import platform
import os
import math


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
        help="Use pyre for increased obfuscation. Linux/WSL only.",
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


def shannon_entropy(file):
    entropy = 0
    with open(file, "rb") as f:
        data = f.read()
        possible = dict(((chr(x), 0) for x in range(0, 256)))
        for byte in data:
            possible[chr(byte)] += 1

        data_len = len(data)
        entropy = 0.0

        # compute
        for i in possible:
            if possible[i] == 0:
                continue

            p = float(possible[i] / data_len)
            entropy -= p * math.log(p, 2)
    return entropy 


def print_stats(in_file, out_file, time):
    in_file_lc = 0
    out_file_lc = 0
    # Calculate line count changes
    with open(in_file, "r") as f:
        in_file_lc = len(f.readlines())
    with open(out_file, "r") as f:
        out_file_lc = len(f.readlines())
    print(f"[*] Obfuscation completed in {time} seconds")
    print(f"[*] Line count: {in_file_lc} -> {out_file_lc} lines")
    # Calculate file size changes 
    in_file_size = os.stat(in_file).st_size
    out_file_size = os.stat(out_file).st_size
    print(f"[*] File size: {in_file_size} -> {out_file_size} bytes")
    in_file_entropy = shannon_entropy(in_file)
    out_file_entropy = shannon_entropy(out_file)
    print(
        f"[*] Shannon entropy: {in_file_entropy} -> "
        f"{out_file_entropy} bits"
    )


def main():
    args = handle_args()
    do_inference = args.inference
    system = platform.system()
    if do_inference is False:
        print("[!] Type inferencing with pyre is not enabled. Obfuscated code may not be reliable.")
    else:
        if system == "Windows":
            print("[!] Pyre is not currently supported on Windows.")
            exit()
        # os.system("pyre")
    start_time = timer()
    # Preprocessing step (we need to write to a temp file in order to make pyre play nice)
    with open(args.in_file, "r", encoding="utf-8") as in_file:
        tree = cst.parse_module(in_file.read())
        transformations = [
            # Seed function definitions and calls with bogus ints for 
            # added obfuscation and more var choices for MBA expressions 
            preprocessing.SeedParams()
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
    temp_file = "jargonaut_tmp.py"
    preprocessed = tree.code 
    with open(temp_file, "w", encoding="utf-8") as out_file:
        out_file.write("# -*- coding: utf-8 -*\n")
        out_file.write(preprocessed)
    print("[-] Finished preprocessing.")
    # HACK: i will handle pyre server setup and configuration later
    if system != "Windows":
        os.system("pyre >> /tmp/out")
    with open(temp_file, "r", encoding="utf-8") as in_file:
        tree = cst.parse_module(in_file.read())
        transformations = [
            # Patch function return values
            control.PatchReturns(),
            # Transform expressions to linear MBAs
            data.ExprToLinearMBA(
                sub_expr_depth=[1, 3],
                super_expr_depth=[1, 5],
                inference=do_inference
            ),
            # Obfuscate builtin calls
            data.HideBuiltinCalls(),
            # Transform integers to linear MBAs
            data.ConstIntToLinearMBA(
                n_terms_range=[4, 5],
                inference=do_inference
            ), 
            # Replace string literals with lambda functions
            data.StringToLambdaExpr(),
            # Remove comments
            layout.RemoveComments(),
            # Insert static opaque MBA predicates
            control.InsertStaticOpaqueMBAPredicates(inference=do_inference),
            # Randomize names
            layout.RandomizeNames(),
            # Remove annotations
            layout.RemoveAnnotations()
    
        ]
        for i, t in enumerate(transformations):
            if do_inference is True:
                manager = FullRepoManager(
                    os.path.dirname(temp_file),
                    {temp_file},
                    {TypeInferenceProvider}
                )
                wrapper = cst.MetadataWrapper(tree, cache=manager.get_cache_for_path(temp_file))
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
        exit()


if __name__ == "__main__":
    main()