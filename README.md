# jargonaut ![pep-8](https://github.com/xor-eax-eax-ret/jargonaut/actions/workflows/pep8.yml/badge.svg)
`jargonaut` is a Python to Python obfuscator with a few cool features. Most of the techniques I have implemented or plan on implementing are ripped from these excellent [University of Arizona lecture slides](https://www2.cs.arizona.edu/~collberg/Teaching/553/2011/Resources/obfuscation.pdf). 

There aren't many Python obfuscators on GitHub that:
- actually produce functional code when some of Python's more complex features are used
- aren't just a combination of variable renaming, Base64 encoding and `marshal`/`eval` spam
- aren't abandoned / deprecated 

This is probably because more advanced obfuscation techniques (especially ones that touch control flow) are pretty difficult to implement for a dynamically typed language that was built around readibility and simplicity! I made `jargonaut` to fill this gap and also to learn more about Python internals, reverse engineering and malware analysis in general. I'm not an expert on any of this, so feel free to propose fixes/new features/improvements! 

Note that this is a proof-of-concept and a work in progress. You should not be using this for anything serious - not only is `jargonaut` probably going to introduce bugs, but deobfuscation will likely be trivial until more features are implemented. 

## Features
- Basic variable, function and parameter renaming (more coming soon)
- Obfuscation of function return values with runtime bytecode patching (work in progress)
- Obfuscation of builtin function calls with `getattr()`
- Multiple string obfuscation methods with lambda expressions and others 
- Obfuscation of arithmetic and bitwise expressions with [linear mixed boolean arithmetic expressions](https://link.springer.com/chapter/10.1007/978-3-540-77535-5_5)

## Planned improvements
### Upcoming features 
- ~Comment removal~
- Type hint removal
- Renaming class methods and attributes with type inferencing
- Opaque predicates/expressions, with and without interdependence
- String obfuscation using Mealy machines
- Packing 
- Bogus control flow 
- Selective virtualization with custom instruction set for functions 
- Dead code/parameter insertion 
- Control flow flattening (chenxification)
- C function conversion a la [pyarmor](https://github.com/dashingsoft/pyarmor)
- Variable splitting/merging
- Function merging 
### Quality of life
- Logging / debugging
- Obfuscation of entire modules, not just single files 
- Documentation 
- Better performance:
    - I'm not using LibCST to its full extent due to lack of knowledge/skill, and I know for a fact the way I perform transformations is suboptimal 
    - I know using Z3 for linear algebra is probably kind of weird and inefficient. I just couldn't figure out how to do it with `numpy` or `scipy` - if you can figure out a better way, please submit a PR! 

## Usage
```
usage: jargonaut [-h] [-in_file IN_FILE] [-out_file OUT_FILE] [--inference]

jargonaut - reliable and configurable Python to Python obfuscation

optional arguments:
  -h, --help          show this help message and exit
  -in_file IN_FILE    path to target file
  -out_file OUT_FILE  path to obfuscated file
  --inference         use pyre's type inference. Linux/WSL only.
```
 
`jargonaut` uses Instagram's [LibCST](https://github.com/Instagram/LibCST) for source code transformations. A transformation is a single operation on the source code's CST, like replacing string literals with obfuscated expressions, or removing comments.

You can configure which transformations are applied and their order of application in `jargonaut.py`

## Requirements 
- z3-solver
- numpy
- libcst

## References
- https://blog.phylum.io/malicious-actors-use-unicode-support-in-python-to-evade-detection
- https://peps.python.org/pep-0672/#normalizing-identifiers
- https://peps.python.org/pep-3131/
- https://unicode.org/reports/tr15/
- https://docs.python.org/3/library/ast.html
- https://link.springer.com/chapter/10.1007/978-3-540-77535-5_5
- https://theses.hal.science/tel-01623849/document
- https://bbs.kanxue.com/thread-271574.htm
- https://libcst.readthedocs.io
- https://www2.cs.arizona.edu/~collberg/Teaching/553/2011/Resources/obfuscation.pdf

## Examples 
View the examples folder if you would like to see this in action. 