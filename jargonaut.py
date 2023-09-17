import os
import platform
import argparse
import math
from timeit import default_timer as timer

import libcst as cst
from libcst.metadata import FullRepoManager, TypeInferenceProvider

from jargonaut.transformations import data, layout, control
from jargonaut import preprocessing


def prompt_for_args():
    args = argparse.Namespace()
    args.in_file = input("Path to target file: ")
    args.out_file = input("Path to obfuscated file: ")
    args.inference = input("Use pyre for increased obfuscation (Linux/WSL only)? (y/n): ").lower() == 'y'
    args.print_stats = input("Print statistics after obfuscation? (y/n): ").lower() == 'y'
    return args


def handle_args():
    parser = argparse.ArgumentParser(prog="jargonaut", description="jargonaut - reliable and configurable Python to Python obfuscation")
    parser.add_argument("-in_file", help="Path to target file")
    parser.add_argument("-out_file", help="Path to obfuscated file")
    parser.add_argument("--inference", default=False, dest="inference", action="store_true",
                        help="Use pyre for increased obfuscation. Linux/WSL only.")
    parser.add_argument("--print-stats", default=True, dest="print_stats", action="store_true",
                        help="Print statistics after obfuscation")
    args = parser.parse_args()
    if not any(vars(args).values()):
        return prompt_for_args()
    return args


def shannon_entropy(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    possible = {chr(x): 0 for x in range(256)}
    for byte in data:
        possible[chr(byte)] += 1
    data_len = len(data)
    return -sum((p / data_len) * math.log(p / data_len, 2) for p in possible.values() if p != 0)


def print_stats(in_file, out_file, elapsed_time):
    in_file_lc = sum(1 for _ in open(in_file, "r"))
    out_file_lc = sum(1 for _ in open(out_file, "r"))
    in_file_size = os.stat(in_file).st_size
    out_file_size = os.stat(out_file).st_size
    in_file_entropy = shannon_entropy(in_file)
    out_file_entropy = shannon_entropy(out_file)

    print(f"[*] Obfuscation completed in {elapsed_time} seconds")
    print(f"[*] Line count: {in_file_lc} -> {out_file_lc} lines")
    print(f"[*] File size: {in_file_size} -> {out_file_size} bytes")
    print(f"[*] Shannon entropy: {in_file_entropy} -> {out_file_entropy} bits")


def apply_transformations(tree, transformations, metadata_wrapper_args=None):
    for t in transformations:
        if metadata_wrapper_args:
            manager = FullRepoManager(*metadata_wrapper_args)
            wrapper = cst.MetadataWrapper(tree, cache=manager.get_cache_for_path(metadata_wrapper_args[1]))
        else:
            wrapper = cst.MetadataWrapper(tree)
        tree = wrapper.visit(t)
        t.spinner.ok()
    return tree


def main():
    args = handle_args()
    system = platform.system()

    if args.inference and system == "Windows":
        print("[!] Pyre is not currently supported on Windows.")
        exit()

    start_time = timer()

    with open(args.in_file, "r", encoding="utf-8") as f:
        tree = cst.parse_module(f.read())

    preprocessing_transformations = [preprocessing.SeedParams(), preprocessing.SeedVars()]

    metadata_wrapper_args = (os.path.dirname(args.in_file), {args.in_file}, {TypeInferenceProvider}) if args.inference else None
    tree = apply_transformations(tree, preprocessing_transformations, metadata_wrapper_args)

    with open("jargonaut_tmp.py", "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*\n")
        f.write(tree.code)

    if system != "Windows":
        os.system("pyre >> /tmp/out")

    with open("jargonaut_tmp.py", "r", encoding="utf-8") as f:
        tree = cst.parse_module(f.read())

    main_transformations = [
        control.PatchReturns(),
        data.ExprToLinearMBA(sub_expr_depth=[1, 3], super_expr_depth=[4, 5], inference=args.inference),
        data.HideBuiltinCalls(),
        data.ConstIntToLinearMBA(n_terms_range=[4, 5], inference=args.inference),
        data.StringToLambdaExpr(),
        layout.RemoveComments(),
        control.InsertStaticOpaqueMBAPredicates(inference=args.inference),
        layout.RandomizeNames(),
        layout.RemoveAnnotations()
    ]

    metadata_wrapper_args = (os.path.dirname("jargonaut_tmp.py"), {"jargonaut_tmp.py"}, {TypeInferenceProvider}) if args.inference else None
    tree = apply_transformations(tree, main_transformations, metadata_wrapper_args)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*\n")
        f.write("import inspect\n")
        f.write("from ctypes import memmove\n")
        f.write(tree.code)

    end_time = timer()

    if args.print_stats:
        print_stats(args.in_file, args.out_file, end_time - start_time)


if __name__ == "__main__":
    main()
