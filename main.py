import sys
from unicloak import unicloak
import ast 


def main():
    if len(sys.argv) != 3:
        print("[!] unicloak.py input_file.py output_file.py")
        exit()
    else:
        with open(sys.argv[1], "r", encoding="utf-8") as in_file:
            uc = unicloak.Unicloak(__builtins__)
            tree = ast.parse(in_file.read())
            tree = ast.fix_missing_locations(uc.visit(tree))
            obfus = ast.unparse(tree)
            with open(sys.argv[2], "w", encoding="utf-8") as out_file:
                # Most specify coding in output file due to binary string obfuscation
                out_file.write("# -*- coding: utf-8 -*\n")
                out_file.write(obfus)


if __name__ == "__main__":
    main()