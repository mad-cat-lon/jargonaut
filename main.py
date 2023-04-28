import sys
from unicloak.transformations import data, layout, control
import ast 


def main():
    if len(sys.argv) != 3:
        print("[!] unicloak.py input_file.py output_file.py")
        exit()
    else:
        with open(sys.argv[1], "r", encoding="utf-8") as in_file:
            
            tree = ast.parse(in_file.read())
            avoid = [
                name for name, func in sorted(vars(__builtins__).items())
            ] 
            transformations = [
                data.LinearMBA(),
                data.BinaryString(),
                layout.ConvertUnicode(),
                layout.RandomizeNames(avoid=avoid)
            ]
            for t in transformations:
                tree = t.visit(tree)
            obfus = ast.unparse(tree)
            with open(sys.argv[2], "w", encoding="utf-8") as out_file:
                # Most specify coding in output file due to binary string obfuscation
                out_file.write("# -*- coding: utf-8 -*\n")
                out_file.write(obfus)


if __name__ == "__main__":
    main()