import sys
from jargonaut.transformations import data, layout, control
import libcst as cst
# from libcst.metadata import FullRepoManager, TypeInferenceProvider


def main():
    if len(sys.argv) != 3:
        print("[!] main.py input_file.py output_file.py")
        exit()
    else:
        with open(sys.argv[1], "r", encoding="utf-8") as in_file:
            tree = cst.parse_module(in_file.read())
            transformations = [
                # Insert custom returns
                control.PatchReturn(),
                # Replace integer literals and binary operations with linear MBAs
                data.LinearMBA(),
                # Replace string literals with lambda functions
                data.LambdaString(),
                # Randomize names
                layout.RandomizeNames(),
                # Remove comments
                layout.RemoveComments()
            ]
            for i, t in enumerate(transformations):
                wrapper = cst.MetadataWrapper(tree)
                tree = wrapper.visit(t)
            obfus = tree
            with open(sys.argv[2], "w", encoding="utf-8") as out_file:
                # Most specify encoding in output file due to binary string obfuscation
                out_file.write("# -*- coding: utf-8 -*\n")
                # For PatchReturn(): this is temporary
                out_file.write("import inspect\n")
                out_file.write("from ctypes import memmove\n")
                out_file.write(obfus.code)
            print("[-] Done.")

if __name__ == "__main__":
    main()