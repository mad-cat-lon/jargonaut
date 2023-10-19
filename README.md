# jargonaut ![pep-8](https://github.com/xor-eax-eax-ret/jargonaut/actions/workflows/pep8.yml/badge.svg) ![license](https://img.shields.io/github/license/mad-cat-lon/jargonaut) ![commits](https://img.shields.io/github/commit-activity/m/mad-cat-lon/jargonaut) ![stars](https://img.shields.io/github/stars/mad-cat-lon/jargonaut?style=social)
`jargonaut` is a Python to Python obfuscator built on Meta's LibCST and the Pyre type checker with a few cool features. Most of the techniques I have implemented or plan on implementing are ripped from these excellent [University of Arizona lecture slides](https://www2.cs.arizona.edu/~collberg/Teaching/553/2011/Resources/obfuscation.pdf). Since Pyre is not supported on Windows, `jargonaut` **is Linux/OSX/WSL only.** `jargonaut` is also only currently capable of **obfuscating individual files. Module-level obfuscation is currently in development.**

There aren't many Python obfuscators on GitHub that:
- actually produce functional code when some of Python's more complex features are used
- aren't just a combination of variable renaming, Base64 encoding and `marshal`/`eval` spam
- aren't abandoned / deprecated 

This is probably because more advanced obfuscation techniques (especially ones that touch control flow) are pretty difficult to implement for a dynamically typed language that was built around readibility and simplicity! I made `jargonaut` to fill this gap and also to learn more about Python internals, linear algebra, reverse engineering and malware analysis in general. I'm not an expert on any of this, so feel free to propose fixes/new features/improvements! 

Note that this is a proof-of-concept and a work in progress. You should not be using this for anything serious - not only is `jargonaut` probably going to introduce bugs, but deobfuscation will likely be trivial until more features are implemented. 

## Features
- Basic variable, function, class and argument renaming 
- Obfuscation of function return values with bytecode patching
- String obfuscation with lambda expressions 
- Dummy argument/variable insertion 
- Basic obfuscation of calls to builtin functions with `getattr`, e.g `print` becomes `getattr(__builtins__, breakpoint.__name__[5]+StopAsyncIteration.__name__[12]+issubclass.__name__[0]+credits.__class__.__name__[4]+AssertionError.__name__[5])`
- Obfuscation of arithmetic/bitwise expressions to [linear mixed boolean arithmetic expressions](https://link.springer.com/chapter/10.1007/978-3-540-77535-5_5)
  - `x ^ y` becomes `(~ (((~ x) ^ y) & (~ (y & (~ (y & (y | ((- y) + (y + y)))))))))`
- Simple obfuscation of integer constants using invertible functions on MBA identities
  - `1337` becomes `((56261358070232866564290277*((1*(x | y)+-1*(x)+-1*(~x | y)+1*(~(x ^ y)))+(291058294156397192947129182780))+(286349190324102644320556429))%2**89)` for any `x, y in Z` 
  - Type inference in `IntConstToMBAExpr` allows us to inspect the current scope, find integer variables and insert them into obfuscated MBA expressions, preventing reverse engineers from simply extracting and evaluating it to obtain the true value. These variables can either be randomly inserted in the preprocessing step or come from the source itself. 
  - Applying `IntConstToMBAExpr()` after `HideBuiltinCalls()` will yield something like the following for `print("Hello world!")`:
  ```
  getattr(__builtins__, KeyboardInterrupt.__name__[((16230303682531376496605*((-1*(136)+-1*(~(136 ^ 870))+-2*(~(136 & 870))+2*(-1)+1*(~870))+(196421983534706283597032))+(24344713766581692105671))%2**75)]+FloatingPointError.__name__[((249081203509*((-2*(487 | ~36)+1*(487)+1*(~(487 ^ 36))+1*(~36))+(910694651731))+(271499565791))%2**38)]+RecursionError.__name__[((7*((2*(~401)+-1*(~(380 | 401))+-2*(380 & ~401)+1*(380 ^ 401)+-1*(~(380 & 401)))+(3319))+(325))%2**10)]+ConnectionError.__name__[((99679084679*((2*(~(68 & 348))+-2*(~348)+-1*(~68 & 348)+1*(68)+-1*(68 | 348))+(364887613628))+(219013332190))%2**38)]+set.__name__[((23166991584907*((1*(~830 | 84)+-1*(~830 & 84)+-1*(-1)+1*(830 ^ 84))+(3122491713942114))+(898265945540812))%2**51)])("Hello world!")
  ```
- Super basic insertion of [static opaque predicates](https://arxiv.org/pdf/1909.01640.pdf) into function bodies, reusing MBA functionality from before 
- Comment removal 

## Planned improvements
### Upcoming features 
- ~Comment removal~
- Array transformation (and transformation of other data to arrays)
- Type hint removal
- Polynomial MBA expressions and more advanced obfuscation rules (**coming soon**)
- Renaming class methods and attributes (**in progress**)
- Opaque predicates/expressions (**in progress**)
  - ~Static opaque MBA predicates~
  - [Dynamic opaque predicates](https://sci-hub.se/https://link.springer.com/chapter/10.1007/978-3-319-45871-7_20)
  - [Opaque predicates with unsolved mathematical conjectures](https://link.springer.com/chapter/10.1007/978-3-642-23822-2_12)
  - [Bi-opaque predicates](https://sci-hub.se/https://ieeexplore.ieee.org/abstract/document/8416525)
- String obfuscation using Mealy machines
- Packing 
- ~Bogus control flow~
- VM obfuscation for selected functions (**in progress, but limited to Python 3.9 bytecode and not compatible with other transformations**)
  - User configurable instruction set and configurable transpiler from Python code -> Python bytecode ->  instruction set for VM
  - Dynamic generation of VM, transpiler and instruction set (really hard)
  - Optional hardening techniques including:
    - Handler randomization / duplication 
    - No central dispatcher by inlining it into each handler(hard)
    - Remove explicit handler table by encoding next handler addresses into instructions 
    - Flow-sensitive instruction decryption to prevent patching and global analyses (really hard)
- ~Dead code/parameter insertion~
- Variable splitting/merging
- Function merging 
### Quality of life
- Logging / debugging
- Unit tests
- Obfuscation of entire modules, not just single files 
- Documentation 
- Better performance:
    - I'm not using LibCST to its full extent due to lack of knowledge/skill, and I know for a fact the way I perform transformations is suboptimal 
    - ~I know using Z3 for linear algebra is probably kind of weird and inefficient. I just couldn't figure out how to do it with `numpy` or `scipy` - if you can figure out a better way, please submit a PR!~ resolved in this [pull request](https://github.com/mad-cat-lon/jargonaut/pull/18)

## Setup 
`jargonaut` uses pyre for type inference. As of right now, pyre is only used during MBA expression generation to avoid transforming string concatenation with variables. If you don't use pyre, **there is a significant chance that the obfuscated code will contain errors and some complex features will not be available.** Also note that pyre is not supported on Windows - for stability, you should be using OSX, Linux or WSL. Instructions for installing and setting up pyre can be found [here](https://pyre-check.org/docs/getting-started/).

After installing pyre, place the file you would like to obfuscate in `jargonaut`'s repo directory and run `pyre init`. The pyre server will then be initialized and monitor the directory for changes during the obfuscation process. Support for files in outside directories and automatic installation, setup and configuaration of pyre will come later. You will need to ensure that the pyre server is started by running `pyre` before running `jargonaut.py`

You can also do the following:
```
git clone https://github.com/mad-cat-lon/jargonaut
cd jargonaut
chmod +x setup.sh
./setup.sh

pyre
cp source_file.py .
python jargonaut.py -in_file source_file.py -out_file obfus_file.py --inference
```
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
 
`jargonaut` uses [LibCST](https://github.com/Instagram/LibCST) for source code transformations. A transformation is a single operation on the source code's CST, like replacing string literals with obfuscated expressions, or removing comments.

You can configure which transformations are applied and their order of application in `jargonaut.py`

## Known/common issues 
- `PatchReturns()` won't work if the obfuscated code is compiled with [Nuitka](https://github.com/Nuitka/Nuitka). This is because the transformation relies on patching function bytecode and Nuitka directly compiles Python to C++. 
- `pyre init` is unable to locate typeshed. To resolve this, clone [typeshed](https://github.com/python/typeshed) and enter the path as `path_to_typeshed/typeshed` and it should work
- File not found error from pyre: This usually happens when a new source file is added to the folder. Do `pyre stop` and `pyre` again to restart the server and let it detect your file.
- Incorrect substitution of variables when `IntConstToMBA()` is applied with `HideBuiltInCalls()`. This happens when names are reused. To prevent this, make sure your variable names are unique across your script! `jargonaut` is not capable of dynamic analysis and it does not know the correct identifier to use in ambiguous cases like in the following:
  ```
  i = 123
  for i in range(10):
    print(i)
  ```



## Examples 
View the examples folder if you would like to see this in action. 

## Requirements 
- z3-solver
- numpy
- libcst
- pyre
- watchman
- yaspin

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
