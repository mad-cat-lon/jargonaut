# jargonaut ![pep-8](https://github.com/xor-eax-eax-ret/jargonaut/actions/workflows/pep8.yml/badge.svg)
`jargonaut` is an obfuscator for protecting Python3 code with a few cool features. Most of the techniques I have implemented or plan on implementing are ripped from these excellent [University of Arizona lecture slides](https://www2.cs.arizona.edu/~collberg/Teaching/553/2011/Resources/obfuscation.pdf). 

There aren't many Python obfuscators on GitHub that:
- actually produce functional code when some of Python's more complex features are used
- aren't just a combination of variable renaming, Base64 encoding and `marshal`/`eval` spam
- aren't abandoned / deprecated 

This is probably because more advanced obfuscation techniques (especially ones that touch control flow) are pretty difficult to implement for a dynamically typed language that was built around readibility and simplicity! `jargonaut` aims to fill this gap - check out the Upcoming Features section for planned additions.

Note that this is a proof-of-concept and a work in progress. You should not be using this for anything serious - not only is `jargonaut` probably going to introduce bugs, but deobfuscation will likely be trivial until more features are implemented. 

## Features
- Basic variable, function and parameter renaming (more coming soon)
- Obfuscation of function return values with runtime bytecode patching (work in progress)
- Multiple string obfuscation methods with lambda expressions and others 
- String matching evasion with [Unicode identifier variants](https://blog.phylum.io/malicious-actors-use-unicode-support-in-python-to-evade-detection)
- Obfuscation of integer literals and expressions with [linear mixed boolean arithmetic expressions](https://link.springer.com/chapter/10.1007/978-3-540-77535-5_5)

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
```main.py source.py obfuscated.py```
`jargonaut` uses Instagram's [LibCST](https://github.com/Instagram/LibCST) for source code transformations. A transformation is a single operation on the source code's CST, like replacing string literals with obfuscated expressions, or removing comments.

You can configure which transformations are applied and their order of application in `main.py`

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
## Example
### Source code
```
import math
class Val:
    def __init__(self, val):
        self.val = val
        self.stringLiteral = "This is a string literal"

    def addOne(self):
        x = self.val + 1 
        return x 
    
    def addVal(self, val):
        x = self.val + val
        self.val = x

    def doMath(self, x):
        return math.log(x, self.val)
    
    def doFormatString(self):
        return f"This is a format string: {self.val}"

class ValSubclass(Val):
    def __init__(self, val):
        super().__init__(val)
        self.subclass = "I am a subclass"

def outside_func(x):
    x = x ** 2
    return x

def higher_order_func(func, x):
    return func(x)

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

if __name__ == "__main__":
    v = Val(2)
    binaryOperation = 1 + 2
    print(v.stringLiteral)
    print(outside_func(v.val))
    print(v.addOne())

    v.addVal(2)
    print(v.val)
    print(v.doFormatString())
    try:
        a = 1 / 0
    except ZeroDivisionError:
        print("This is an exception")
    print(higher_order_func(lambda x: x**2, 3))
    x = ValSubclass(2)
    print(x.subclass)
    print(factorial(10))
```
### Obfuscated code
```
# -*- coding: utf-8 -*
import inspect
from ctypes import memmove
import math

class IillliIIlliI:
    def __init__(self, illllliIIIII):
        self.val = illllliIIIII
        self.stringLiteral = (lambda lIilllIlIiIi, iiiIiilIlIli, IllliIIIilIi, iIIllliiiliI, llIIiIIlIlil, llilIlIillll, IIiIiIIlilll, lilIiIllIiII:    (lambda liIIlIllIliI, iiIIllIillii, liiilillIiIi: liIIlIllIliI(liIIlIllIliI, iiIIllIillii, liiilillIiIi))(            lambda liIIlIllIliI, iiIIllIillii, liiilillIiIi:                bytes([liiilillIiIi % iiIIllIillii]) + liIIlIllIliI(liIIlIllIliI, iiIIllIillii, liiilillIiIi // iiIIllIillii) if liiilillIiIi else                (lambda: liIIlIllIliI).__code__.co_lnotab,            lIilllIlIiIi << lilIiIllIiII,            (((((lIilllIlIiIi << iIIllliiiliI) + lIilllIlIiIi) << iIIllliiiliI) + IllliIIIilIi) << ((IllliIIIilIi << llilIlIillll) + llIIiIIlIlil)) + (((IllliIIIilIi << llIIiIIlIlil) + IllliIIIilIi) << ((IllliIIIilIi << llilIlIillll) - IllliIIIilIi)) + (((IllliIIIilIi << llilIlIillll) - IIiIiIIlilll) << ((((IllliIIIilIi << iiiIiilIlIli) - lIilllIlIiIi) << iIIllliiiliI) + lIilllIlIiIi)) + (((((IllliIIIilIi << iiiIiilIlIli) + lIilllIlIiIi) << iIIllliiiliI) - llIIiIIlIlil) << ((llIIiIIlIlil << llIIiIIlIlil) + IIiIiIIlilll)) - (((IllliIIIilIi << llilIlIillll) - IIiIiIIlilll) << ((llIIiIIlIlil << llIIiIIlIlil) - (lIilllIlIiIi << iiiIiilIlIli))) - (((((IllliIIIilIi << iiiIiilIlIli) + lIilllIlIiIi) << IllliIIIilIi) + lIilllIlIiIi) << (((((lIilllIlIiIi << IllliIIIilIi) + lIilllIlIiIi)) << iIIllliiiliI) + (lIilllIlIiIi << iiiIiilIlIli))) - (((lIilllIlIiIi << llIIiIIlIlil) - lIilllIlIiIi) << (((((lIilllIlIiIi << IllliIIIilIi) + lIilllIlIiIi)) << iIIllliiiliI) - IllliIIIilIi)) + (((((IllliIIIilIi << iiiIiilIlIli) + lIilllIlIiIi) << iIIllliiiliI) - lIilllIlIiIi) << ((lIilllIlIiIi << IIiIiIIlilll) - lIilllIlIiIi)) - ((((((lIilllIlIiIi << IllliIIIilIi) + lIilllIlIiIi)) << iIIllliiiliI) - IllliIIIilIi) << ((((lIilllIlIiIi << iIIllliiiliI) - lIilllIlIiIi) << IllliIIIilIi) - IllliIIIilIi)) + (((((llIIiIIlIlil << iiiIiilIlIli) - lIilllIlIiIi) << IllliIIIilIi) - lIilllIlIiIi) << ((IIiIiIIlilll << iIIllliiiliI) - (lIilllIlIiIi << iiiIiilIlIli))) + (((llIIiIIlIlil << llIIiIIlIlil) - IllliIIIilIi) << ((IllliIIIilIi << llIIiIIlIlil) + (lIilllIlIiIi << lIilllIlIiIi))) + (((IIiIiIIlilll << iIIllliiiliI) + IllliIIIilIi) << ((((IllliIIIilIi << iiiIiilIlIli) - lIilllIlIiIi) << IllliIIIilIi))) + (((lIilllIlIiIi << llilIlIillll) + lIilllIlIiIi) << ((llIIiIIlIlil << iIIllliiiliI) - lIilllIlIiIi)) - (((((lIilllIlIiIi << iIIllliiiliI) - lIilllIlIiIi) << IllliIIIilIi) + IllliIIIilIi) << (((((lIilllIlIiIi << IllliIIIilIi) + lIilllIlIiIi)) << IllliIIIilIi) - (lIilllIlIiIi << lIilllIlIiIi))) - (((lIilllIlIiIi << llilIlIillll) - lIilllIlIiIi) << ((lIilllIlIiIi << llilIlIillll) - lIilllIlIiIi)) - (((((IllliIIIilIi << iiiIiilIlIli) + lIilllIlIiIi) << IllliIIIilIi) - IllliIIIilIi) << ((((IllliIIIilIi << iiiIiilIlIli) + lIilllIlIiIi) << iiiIiilIlIli) + lIilllIlIiIi)) + ((((((lIilllIlIiIi << IllliIIIilIi) + lIilllIlIiIi)) << IllliIIIilIi) + lIilllIlIiIi) << ((((IllliIIIilIi << iiiIiilIlIli) - lIilllIlIiIi) << iiiIiilIlIli) + lIilllIlIiIi)) + (((IIiIiIIlilll << iiiIiilIlIli) + lIilllIlIiIi) << ((lIilllIlIiIi << llIIiIIlIlil) + (lIilllIlIiIi << lIilllIlIiIi))) - (((llIIiIIlIlil << iiiIiilIlIli) - lIilllIlIiIi) << ((IIiIiIIlilll << iiiIiilIlIli) - lIilllIlIiIi)) + (((((IllliIIIilIi << iiiIiilIlIli) - lIilllIlIiIi) << iiiIiilIlIli) + lIilllIlIiIi) << ((llIIiIIlIlil << iiiIiilIlIli) - lIilllIlIiIi)) + (((llIIiIIlIlil << iiiIiilIlIli) + lIilllIlIiIi) << ((llIIiIIlIlil << lIilllIlIiIi))) + (((lIilllIlIiIi << iIIllliiiliI) + lIilllIlIiIi) << lIilllIlIiIi)        )    )(        *(lambda lIilllIlIiIi, iiiIiilIlIli, IllliIIIilIi: lIilllIlIiIi(lIilllIlIiIi, iiiIiilIlIli, IllliIIIilIi))(            (lambda lIilllIlIiIi, iiiIiilIlIli, IllliIIIilIi:                [iiiIiilIlIli(IllliIIIilIi[(lambda: lIilllIlIiIi).__code__.co_nlocals])] +                lIilllIlIiIi(lIilllIlIiIi, iiiIiilIlIli, IllliIIIilIi[(lambda liIIlIllIliI: liIIlIllIliI).__code__.co_nlocals:]) if IllliIIIilIi else []            ),            lambda lIilllIlIiIi: lIilllIlIiIi.__code__.co_argcount,            (                lambda lIilllIlIiIi: lIilllIlIiIi,                lambda lIilllIlIiIi, iiiIiilIlIli: lIilllIlIiIi,                lambda lIilllIlIiIi, iiiIiilIlIli, IllliIIIilIi: lIilllIlIiIi,                lambda lIilllIlIiIi, iiiIiilIlIli, IllliIIIilIi, iIIllliiiliI: lIilllIlIiIi,                lambda lIilllIlIiIi, iiiIiilIlIli, IllliIIIilIi, iIIllliiiliI, llIIiIIlIlil: lIilllIlIiIi,                lambda lIilllIlIiIi, iiiIiilIlIli, IllliIIIilIi, iIIllliiiliI, llIIiIIlIlil, llilIlIillll: lIilllIlIiIi,                lambda lIilllIlIiIi, iiiIiilIlIli, IllliIIIilIi, iIIllliiiliI, llIIiIIlIlil, llilIlIillll, IIiIiIIlilll: lIilllIlIiIi,                lambda lIilllIlIiIi, iiiIiilIlIli, IllliIIIilIi, iIIllliiiliI, llIIiIIlIlil, llilIlIillll, IIiIiIIlilll, lilIiIllIiII: lIilllIlIiIi            )        )    ).decode("utf-8")[1:-1]

    def addOne(self):
        lililillilIi = (-2 * (self.val & 1) + -5 * (~self.val & 1) + 7 * 1 + -1 * (self.val | 1) + -2 * ~(self.val ^ 1) + 2 * ~1) 
        def iIIlIIIliili(lliIlliIiIiI):
            liIIlIlilIIi = inspect.currentframe().f_back
            IlliliIIiiII = liIIlIlilIIi.f_code.co_code
            IllIiIIlIlli = liIIlIlilIIi.f_lasti
            iiiIIliiiIlI = bytes(IlliliIIiiII)
            memmove((-1 * (id(iiiIIliiiIlI) & 0x20) + -4 * (id(iiiIIliiiIlI) & ~0x20) + 4 * id(iiiIIliiiIlI) + 1 * (~id(iiiIIliiiIlI) & 0x20) + -1 * ~(id(iiiIIliiiIlI) ^ 0x20) + 1 * ~0x20) + IllIiIIlIlli + (1 * (31415 & 999) + -1 * 31415 + -1 * (~31415 & 999) + 1 * (31415 ^ 999) + -2 * -1), b"\x53\x00", (-1 * 1337 + 3 * (999 ^ 1337) + -2 * (999 | 1337) + -2 * ~(999 | 1337) + 3 * ~(999 ^ 1337) + -1 * ~1337 + -2 * -1))
            return lliIlliIiIiI
        iIIlIIIliili(lililillilIi)
        return (lambda iiiiIllliIIi, llilIIilllll, iIIiIllIlilI, IilliiilIIii, iiiIllIIlllI, lliilIiIIllI, lIlliilillIi, lIiilliilill:    (lambda IIIIIIlilIll, iiiiiIlIlIII, liIilllIiIIl: IIIIIIlilIll(IIIIIIlilIll, iiiiiIlIlIII, liIilllIiIIl))(            lambda IIIIIIlilIll, iiiiiIlIlIII, liIilllIiIIl:                bytes([liIilllIiIIl % iiiiiIlIlIII]) + IIIIIIlilIll(IIIIIIlilIll, iiiiiIlIlIII, liIilllIiIIl // iiiiiIlIlIII) if liIilllIiIIl else                (lambda: IIIIIIlilIll).__code__.co_lnotab,            iiiiIllliIIi << lIiilliilill,            (((((iiiiIllliIIi << IilliiilIIii) + iiiiIllliIIi) << iIIiIllIlilI) + iiiiIllliIIi) << ((iiiIllIIlllI << IilliiilIIii) - (iiiiIllliIIi << iiiiIllliIIi))) + (((iIIiIllIlilI << IilliiilIIii) + iiiiIllliIIi) << (((((iiiiIllliIIi << iIIiIllIlilI) + iiiiIllliIIi)) << iIIiIllIlilI) - (iiiiIllliIIi << iiiiIllliIIi))) + (((((iiiiIllliIIi << IilliiilIIii) - iiiiIllliIIi) << llilIIilllll) + iiiiIllliIIi) << ((iiiiIllliIIi << lliilIiIIllI) - (iiiiIllliIIi << iiiiIllliIIi))) + (((iIIiIllIlilI << IilliiilIIii) + iiiiIllliIIi) << ((lIlliilillIi << iIIiIllIlilI) - (iiiiIllliIIi << iiiiIllliIIi))) + (((((iiiiIllliIIi << IilliiilIIii) - iiiiIllliIIi) << llilIIilllll) + iiiiIllliIIi) << ((iIIiIllIlilI << IilliiilIIii) - (iiiiIllliIIi << iiiiIllliIIi))) + (((iIIiIllIlilI << IilliiilIIii) + iiiiIllliIIi) << ((iiiIllIIlllI << iIIiIllIlilI) - (iiiiIllliIIi << iiiiIllliIIi))) + (((((iiiiIllliIIi << IilliiilIIii) - iiiiIllliIIi) << llilIIilllll) + iiiiIllliIIi) << ((((iiiiIllliIIi << IilliiilIIii) - iiiiIllliIIi) << iiiiIllliIIi))) + (((iIIiIllIlilI << IilliiilIIii) + iiiiIllliIIi) << ((((iIIiIllIlilI << llilIIilllll) - iiiiIllliIIi) << iiiiIllliIIi))) + (((iiiiIllliIIi << iiiIllIIlllI) - iiiiIllliIIi) << ((iiiiIllliIIi << IilliiilIIii) - iiiiIllliIIi)) - ((((iIIiIllIlilI << llilIIilllll) + iiiiIllliIIi)) << ((iiiIllIIlllI << iiiiIllliIIi))) + (((iiiiIllliIIi << IilliiilIIii) + iiiiIllliIIi) << iiiiIllliIIi)        )    )(        *(lambda iiiiIllliIIi, llilIIilllll, iIIiIllIlilI: iiiiIllliIIi(iiiiIllliIIi, llilIIilllll, iIIiIllIlilI))(            (lambda iiiiIllliIIi, llilIIilllll, iIIiIllIlilI:                [llilIIilllll(iIIiIllIlilI[(lambda: iiiiIllliIIi).__code__.co_nlocals])] +                iiiiIllliIIi(iiiiIllliIIi, llilIIilllll, iIIiIllIlilI[(lambda IIIIIIlilIll: IIIIIIlilIll).__code__.co_nlocals:]) if iIIiIllIlilI else []            ),            lambda iiiiIllliIIi: iiiiIllliIIi.__code__.co_argcount,            (                lambda iiiiIllliIIi: iiiiIllliIIi,                lambda iiiiIllliIIi, llilIIilllll: iiiiIllliIIi,                lambda iiiiIllliIIi, llilIIilllll, iIIiIllIlilI: iiiiIllliIIi,                lambda iiiiIllliIIi, llilIIilllll, iIIiIllIlilI, IilliiilIIii: iiiiIllliIIi,                lambda iiiiIllliIIi, llilIIilllll, iIIiIllIlilI, IilliiilIIii, iiiIllIIlllI: iiiiIllliIIi,                lambda iiiiIllliIIi, llilIIilllll, iIIiIllIlilI, IilliiilIIii, iiiIllIIlllI, lliilIiIIllI: iiiiIllliIIi,                lambda iiiiIllliIIi, llilIIilllll, iIIiIllIlilI, IilliiilIIii, iiiIllIIlllI, lliilIiIIllI, lIlliilillIi: iiiiIllliIIi,                lambda iiiiIllliIIi, llilIIilllll, iIIiIllIlilI, IilliiilIIii, iiiIllIIlllI, lliilIiIIllI, lIlliilillIi, lIiilliilill: iiiiIllliIIi            )        )    ).decode("utf-8")[1:-1]
    
    def addVal(self, IIlliIillili):
        IliiIIiIilll = (-1 * (self.val & IIlliIillili) + 3 * (self.val & ~IIlliIillili) + 1 * self.val + 4 * IIlliIillili + -2 * (self.val ^ IIlliIillili) + -1 * (self.val | IIlliIillili) + 1 * ~(self.val | IIlliIillili) + -1 * ~(self.val ^ IIlliIillili))
        self.val = IliiIIiIilll

    def doMath(self, iiiilIliiiii):
        def IilIliIilIiI(iililliIlllI):
            iiIIlllIiiIl = inspect.currentframe().f_back
            IiiliIiliIii = iiIIlllIiiIl.f_code.co_code
            IIiIillIIIiI = iiIIlllIiiIl.f_lasti
            lillIIillliI = bytes(IiiliIiliIii)
            memmove((-2 * (id(lillIIillliI) & 0x20) + -5 * (id(lillIIillliI) & ~0x20) + 6 * id(lillIIillliI) + 2 * (~id(lillIIillliI) & 0x20) + -1 * 0x20 + 1 * ~(id(lillIIillliI) | 0x20) + -1 * ~(id(lillIIillliI) ^ 0x20)) + IIiIillIIIiI + (-2 * (1337 & 1984) + -4 * (1337 & ~1984) + -2 * (~1337 & 1984) + -1 * 1984 + 3 * (1337 | 1984) + -1 * ~(1337 | 1984) + 1 * ~1984 + -2 * -1), b"\x53\x00", (2 * (420 & 747) + -1 * (420 & ~747) + 1 * ~(420 | 747) + -2 * ~(420 ^ 747) + 1 * ~747 + -2 * -1))
            return iililliIlllI
        IilIliIilIiI(math.log(iiiilIliiiii, self.val))
        return (lambda IlliliiIIIli, lIIliilIlIll, IllIllIiIIll, IliIIiilillI, IIiiIIlIIllI, IiIillIilIli, iilIllIiilII, IiIlliIIiiIi:    (lambda llililiiIilI, liIliiIiiIIl, ililIIIliiII: llililiiIilI(llililiiIilI, liIliiIiiIIl, ililIIIliiII))(            lambda llililiiIilI, liIliiIiiIIl, ililIIIliiII:                bytes([ililIIIliiII % liIliiIiiIIl]) + llililiiIilI(llililiiIilI, liIliiIiiIIl, ililIIIliiII // liIliiIiiIIl) if ililIIIliiII else                (lambda: llililiiIilI).__code__.co_lnotab,            IlliliiIIIli << IiIlliIIiiIi,            (((((IlliliiIIIli << IliIIiilillI) + IlliliiIIIli) << IllIllIiIIll) + IlliliiIIIli) << ((IIiiIIlIIllI << IliIIiilillI) - (IlliliiIIIli << IlliliiIIIli))) + (((IllIllIiIIll << IliIIiilillI) + IlliliiIIIli) << (((((IlliliiIIIli << IllIllIiIIll) + IlliliiIIIli)) << IllIllIiIIll) - (IlliliiIIIli << IlliliiIIIli))) + (((((IlliliiIIIli << IliIIiilillI) - IlliliiIIIli) << lIIliilIlIll) + IlliliiIIIli) << ((IlliliiIIIli << IiIillIilIli) - (IlliliiIIIli << IlliliiIIIli))) + (((IllIllIiIIll << IliIIiilillI) + IlliliiIIIli) << ((iilIllIiilII << IllIllIiIIll) - (IlliliiIIIli << IlliliiIIIli))) + (((((IlliliiIIIli << IliIIiilillI) - IlliliiIIIli) << lIIliilIlIll) + IlliliiIIIli) << ((IllIllIiIIll << IliIIiilillI) - (IlliliiIIIli << IlliliiIIIli))) + (((IllIllIiIIll << IliIIiilillI) + IlliliiIIIli) << ((IIiiIIlIIllI << IllIllIiIIll) - (IlliliiIIIli << IlliliiIIIli))) + (((((IlliliiIIIli << IliIIiilillI) - IlliliiIIIli) << lIIliilIlIll) + IlliliiIIIli) << ((((IlliliiIIIli << IliIIiilillI) - IlliliiIIIli) << IlliliiIIIli))) + (((IllIllIiIIll << IliIIiilillI) + IlliliiIIIli) << ((((IllIllIiIIll << lIIliilIlIll) - IlliliiIIIli) << IlliliiIIIli))) + (((IlliliiIIIli << IIiiIIlIIllI) - IlliliiIIIli) << ((IlliliiIIIli << IliIIiilillI) - IlliliiIIIli)) - ((((IllIllIiIIll << lIIliilIlIll) + IlliliiIIIli)) << ((IIiiIIlIIllI << IlliliiIIIli))) + (((IlliliiIIIli << IliIIiilillI) + IlliliiIIIli) << IlliliiIIIli)        )    )(        *(lambda IlliliiIIIli, lIIliilIlIll, IllIllIiIIll: IlliliiIIIli(IlliliiIIIli, lIIliilIlIll, IllIllIiIIll))(            (lambda IlliliiIIIli, lIIliilIlIll, IllIllIiIIll:                [lIIliilIlIll(IllIllIiIIll[(lambda: IlliliiIIIli).__code__.co_nlocals])] +                IlliliiIIIli(IlliliiIIIli, lIIliilIlIll, IllIllIiIIll[(lambda llililiiIilI: llililiiIilI).__code__.co_nlocals:]) if IllIllIiIIll else []            ),            lambda IlliliiIIIli: IlliliiIIIli.__code__.co_argcount,            (                lambda IlliliiIIIli: IlliliiIIIli,                lambda IlliliiIIIli, lIIliilIlIll: IlliliiIIIli,                lambda IlliliiIIIli, lIIliilIlIll, IllIllIiIIll: IlliliiIIIli,                lambda IlliliiIIIli, lIIliilIlIll, IllIllIiIIll, IliIIiilillI: IlliliiIIIli,                lambda IlliliiIIIli, lIIliilIlIll, IllIllIiIIll, IliIIiilillI, IIiiIIlIIllI: IlliliiIIIli,                lambda IlliliiIIIli, lIIliilIlIll, IllIllIiIIll, IliIIiilillI, IIiiIIlIIllI, IiIillIilIli: IlliliiIIIli,                lambda IlliliiIIIli, lIIliilIlIll, IllIllIiIIll, IliIIiilillI, IIiiIIlIIllI, IiIillIilIli, iilIllIiilII: IlliliiIIIli,                lambda IlliliiIIIli, lIIliilIlIll, IllIllIiIIll, IliIIiilillI, IIiiIIlIIllI, IiIillIilIli, iilIllIiilII, IiIlliIIiiIi: IlliliiIIIli            )        )    ).decode("utf-8")[1:-1]
    
    def doFormatString(self):
        def iIilIIlliIiI(lllliIiIIIil):
            iIlIlIliiill = inspect.currentframe().f_back
            iilIIililiIl = iIlIlIliiill.f_code.co_code
            liililiIiilI = iIlIlIliiill.f_lasti
            IiiIiIilllll = bytes(iilIIililiIl)
            memmove((-3 * (id(IiiIiIilllll) & 0x20) + -1 * (id(IiiIiIilllll) & ~0x20) + 3 * id(IiiIiIilllll) + 2 * 0x20 + -1 * (id(IiiIiIilllll) ^ 0x20)) + liililiIiilI + (-1 * (31415 & 1337) + 1 * (~31415 & 1337) + -2 * (31415 ^ 1337) + 1 * (31415 | 1337) + -1 * ~(31415 | 1337) + 1 * ~1337 + -2 * -1), b"\x53\x00", (-3 * (420 & ~999) + 3 * 420 + 3 * (~420 & 999) + -2 * 999 + -1 * (420 ^ 999) + -1 * ~(420 ^ 999) + 1 * ~999 + -2 * -1))
            return lllliIiIIIil
        iIilIIlliIiI(f"This is a format string: {self.val}")
        return (lambda iliIIiIiliiI, IIIlllIIiIll, IliilllIIIIl, IllIliiliiIl, iillilllilii, lIliilIliiII, iIiilililIlI, IllllIiIiiII:    (lambda lilIlilIliII, lliIlIiIIlIl, iIIliIIllIli: lilIlilIliII(lilIlilIliII, lliIlIiIIlIl, iIIliIIllIli))(            lambda lilIlilIliII, lliIlIiIIlIl, iIIliIIllIli:                bytes([iIIliIIllIli % lliIlIiIIlIl]) + lilIlilIliII(lilIlilIliII, lliIlIiIIlIl, iIIliIIllIli // lliIlIiIIlIl) if iIIliIIllIli else                (lambda: lilIlilIliII).__code__.co_lnotab,            iliIIiIiliiI << IllllIiIiiII,            (((((iliIIiIiliiI << IllIliiliiIl) + iliIIiIiliiI) << IliilllIIIIl) + iliIIiIiliiI) << ((iillilllilii << IllIliiliiIl) - (iliIIiIiliiI << iliIIiIiliiI))) + (((IliilllIIIIl << IllIliiliiIl) + iliIIiIiliiI) << (((((iliIIiIiliiI << IliilllIIIIl) + iliIIiIiliiI)) << IliilllIIIIl) - (iliIIiIiliiI << iliIIiIiliiI))) + (((((iliIIiIiliiI << IllIliiliiIl) - iliIIiIiliiI) << IIIlllIIiIll) + iliIIiIiliiI) << ((iliIIiIiliiI << lIliilIliiII) - (iliIIiIiliiI << iliIIiIiliiI))) + (((IliilllIIIIl << IllIliiliiIl) + iliIIiIiliiI) << ((iIiilililIlI << IliilllIIIIl) - (iliIIiIiliiI << iliIIiIiliiI))) + (((((iliIIiIiliiI << IllIliiliiIl) - iliIIiIiliiI) << IIIlllIIiIll) + iliIIiIiliiI) << ((IliilllIIIIl << IllIliiliiIl) - (iliIIiIiliiI << iliIIiIiliiI))) + (((IliilllIIIIl << IllIliiliiIl) + iliIIiIiliiI) << ((iillilllilii << IliilllIIIIl) - (iliIIiIiliiI << iliIIiIiliiI))) + (((((iliIIiIiliiI << IllIliiliiIl) - iliIIiIiliiI) << IIIlllIIiIll) + iliIIiIiliiI) << ((((iliIIiIiliiI << IllIliiliiIl) - iliIIiIiliiI) << iliIIiIiliiI))) + (((IliilllIIIIl << IllIliiliiIl) + iliIIiIiliiI) << ((((IliilllIIIIl << IIIlllIIiIll) - iliIIiIiliiI) << iliIIiIiliiI))) + (((iliIIiIiliiI << iillilllilii) - iliIIiIiliiI) << ((iliIIiIiliiI << IllIliiliiIl) - iliIIiIiliiI)) - ((((IliilllIIIIl << IIIlllIIiIll) + iliIIiIiliiI)) << ((iillilllilii << iliIIiIiliiI))) + (((iliIIiIiliiI << IllIliiliiIl) + iliIIiIiliiI) << iliIIiIiliiI)        )    )(        *(lambda iliIIiIiliiI, IIIlllIIiIll, IliilllIIIIl: iliIIiIiliiI(iliIIiIiliiI, IIIlllIIiIll, IliilllIIIIl))(            (lambda iliIIiIiliiI, IIIlllIIiIll, IliilllIIIIl:                [IIIlllIIiIll(IliilllIIIIl[(lambda: iliIIiIiliiI).__code__.co_nlocals])] +                iliIIiIiliiI(iliIIiIiliiI, IIIlllIIiIll, IliilllIIIIl[(lambda lilIlilIliII: lilIlilIliII).__code__.co_nlocals:]) if IliilllIIIIl else []            ),            lambda iliIIiIiliiI: iliIIiIiliiI.__code__.co_argcount,            (                lambda iliIIiIiliiI: iliIIiIiliiI,                lambda iliIIiIiliiI, IIIlllIIiIll: iliIIiIiliiI,                lambda iliIIiIiliiI, IIIlllIIiIll, IliilllIIIIl: iliIIiIiliiI,                lambda iliIIiIiliiI, IIIlllIIiIll, IliilllIIIIl, IllIliiliiIl: iliIIiIiliiI,                lambda iliIIiIiliiI, IIIlllIIiIll, IliilllIIIIl, IllIliiliiIl, iillilllilii: iliIIiIiliiI,                lambda iliIIiIiliiI, IIIlllIIiIll, IliilllIIIIl, IllIliiliiIl, iillilllilii, lIliilIliiII: iliIIiIiliiI,                lambda iliIIiIiliiI, IIIlllIIiIll, IliilllIIIIl, IllIliiliiIl, iillilllilii, lIliilIliiII, iIiilililIlI: iliIIiIiliiI,                lambda iliIIiIiliiI, IIIlllIIiIll, IliilllIIIIl, IllIliiliiIl, iillilllilii, lIliilIliiII, iIiilililIlI, IllllIiIiiII: iliIIiIiliiI            )        )    ).decode("utf-8")[1:-1]

class iIlIIiIIlIil(IillliIIlliI):
    def __init__(self, iiliiiiiIlll):
        super().__init__(iiliiiiiIlll)
        self.subclass = (lambda iillIillIIIi, IiIiiIiliIll, lIiliIlIIIiI, iIlIliliIlII, llIlIillIlll, liilIIiillii, lIlIliiilill, iliiIlIIiIiI:    (lambda llIllilIiIII, lllIIIlliiIl, IlIiIiIiliiI: llIllilIiIII(llIllilIiIII, lllIIIlliiIl, IlIiIiIiliiI))(            lambda llIllilIiIII, lllIIIlliiIl, IlIiIiIiliiI:                bytes([IlIiIiIiliiI % lllIIIlliiIl]) + llIllilIiIII(llIllilIiIII, lllIIIlliiIl, IlIiIiIiliiI // lllIIIlliiIl) if IlIiIiIiliiI else                (lambda: llIllilIiIII).__code__.co_lnotab,            iillIillIIIi << iliiIlIIiIiI,            (((((iillIillIIIi << iIlIliliIlII) + iillIillIIIi) << IiIiiIiliIll) + iillIillIIIi) << ((iillIillIIIi << lIlIliiilill) - iillIillIIIi)) - (((((lIiliIlIIIiI << IiIiiIiliIll) + iillIillIIIi) << iIlIliliIlII) - lIlIliiilill) << ((lIlIliiilill << iIlIliliIlII) + (iillIillIIIi << IiIiiIiliIll))) + (((lIlIliiilill << IiIiiIiliIll) - iillIillIIIi) << ((lIlIliiilill << iIlIliliIlII) - lIiliIlIIIiI)) + (((((lIiliIlIIIiI << IiIiiIiliIll) - iillIillIIIi) << lIiliIlIIIiI) + lIiliIlIIIiI) << ((lIiliIlIIIiI << llIlIillIlll) + (iillIillIIIi << iillIillIIIi))) + (((lIiliIlIIIiI << llIlIillIlll) + lIiliIlIIIiI) << ((((lIiliIlIIIiI << IiIiiIiliIll) - iillIillIIIi) << lIiliIlIIIiI))) + (((lIiliIlIIIiI << iIlIliliIlII) + iillIillIIIi) << ((llIlIillIlll << iIlIliliIlII) + iillIillIIIi)) + (((((iillIillIIIi << iIlIliliIlII) - iillIillIIIi) << lIiliIlIIIiI) - lIiliIlIIIiI) << (((((iillIillIIIi << lIiliIlIIIiI) + iillIillIIIi)) << lIiliIlIIIiI))) + (((lIlIliiilill << iIlIliliIlII) + lIiliIlIIIiI) << ((iillIillIIIi << liilIIiillii))) + (((iillIillIIIi << liilIIiillii) + iillIillIIIi) << ((lIlIliiilill << lIiliIlIIIiI) - iillIillIIIi)) - (((iillIillIIIi << llIlIillIlll) - iillIillIIIi) << ((lIiliIlIIIiI << iIlIliliIlII))) + (((iillIillIIIi << liilIIiillii) + iillIillIIIi) << ((llIlIillIlll << lIiliIlIIIiI) - iillIillIIIi)) - ((((((iillIillIIIi << lIiliIlIIIiI) + iillIillIIIi)) << IiIiiIiliIll) + iillIillIIIi) << ((iillIillIIIi << llIlIillIlll) - iillIillIIIi)) - (((iillIillIIIi << llIlIillIlll) - iillIillIIIi) << ((lIiliIlIIIiI << lIiliIlIIIiI))) + (iillIillIIIi << ((llIlIillIlll << IiIiiIiliIll) + iillIillIIIi)) + ((((((iillIillIIIi << lIiliIlIIIiI) + iillIillIIIi)) << IiIiiIiliIll) + iillIillIIIi) << ((((iillIillIIIi << lIiliIlIIIiI) + iillIillIIIi)))) - (lIlIliiilill << llIlIillIlll) + (iillIillIIIi << iillIillIIIi)        )    )(        *(lambda iillIillIIIi, IiIiiIiliIll, lIiliIlIIIiI: iillIillIIIi(iillIillIIIi, IiIiiIiliIll, lIiliIlIIIiI))(            (lambda iillIillIIIi, IiIiiIiliIll, lIiliIlIIIiI:                [IiIiiIiliIll(lIiliIlIIIiI[(lambda: iillIillIIIi).__code__.co_nlocals])] +                iillIillIIIi(iillIillIIIi, IiIiiIiliIll, lIiliIlIIIiI[(lambda llIllilIiIII: llIllilIiIII).__code__.co_nlocals:]) if lIiliIlIIIiI else []            ),            lambda iillIillIIIi: iillIillIIIi.__code__.co_argcount,            (                lambda iillIillIIIi: iillIillIIIi,                lambda iillIillIIIi, IiIiiIiliIll: iillIillIIIi,                lambda iillIillIIIi, IiIiiIiliIll, lIiliIlIIIiI: iillIillIIIi,                lambda iillIillIIIi, IiIiiIiliIll, lIiliIlIIIiI, iIlIliliIlII: iillIillIIIi,                lambda iillIillIIIi, IiIiiIiliIll, lIiliIlIIIiI, iIlIliliIlII, llIlIillIlll: iillIillIIIi,                lambda iillIillIIIi, IiIiiIiliIll, lIiliIlIIIiI, iIlIliliIlII, llIlIillIlll, liilIIiillii: iillIillIIIi,                lambda iillIillIIIi, IiIiiIiliIll, lIiliIlIIIiI, iIlIliliIlII, llIlIillIlll, liilIIiillii, lIlIliiilill: iillIillIIIi,                lambda iillIillIIIi, IiIiiIiliIll, lIiliIlIIIiI, iIlIliliIlII, llIlIillIlll, liilIIiillii, lIlIliiilill, iliiIlIIiIiI: iillIillIIIi            )        )    ).decode("utf-8")[1:-1]

def illIiiIiIiIi(lliiiiIIlIIi):
    lliiiiIIlIIi = lliiiiIIlIIi ** (1 * (999 & ~747) + -1 * (~999 & 747) + 5 * 747 + -1 * (999 ^ 747) + -3 * (999 | 747) + -1 * ~(999 | 747) + -2 * ~(999 ^ 747) + 3 * ~747 + -2 * -1)
    def liiIIIIiliiI(lIIIlilIiiIl):
        lIIlIlliIIlI = inspect.currentframe().f_back
        iiIIliIIllII = lIIlIlliIIlI.f_code.co_code
        IilliIllilIl = lIIlIlliIIlI.f_lasti
        iIilIiiiIIIi = bytes(iiIIliIIllII)
        memmove((-1 * (id(iIilIiiiIIIi) & 0x20) + 2 * id(iIilIiiiIIIi) + 2 * 0x20 + -1 * (id(iIilIiiiIIIi) | 0x20)) + IilliIllilIl + (-1 * (420 & 1337) + -2 * 1337 + 2 * (420 | 1337) + 1 * ~(420 | 1337) + 1 * ~(420 ^ 1337) + -2 * ~1337 + -2 * -1), b"\x53\x00", (5 * (31415 & 1337) + -1 * (31415 & ~1337) + -1 * 31415 + -2 * 1337 + 2 * (31415 ^ 1337) + 2 * ~(31415 | 1337) + -2 * ~(31415 ^ 1337) + -2 * -1))
        return lIIIlilIiiIl
    liiIIIIiliiI(lliiiiIIlIIi)
    return (lambda iliiiIIliilI, lIlliIiliili, iiIlllIiIill, iIllllilliil, llIIIliIIIII, iiIllIlIiIIl, IIIIilIliiIi, lIiiliIIIlIl:    (lambda IiilIiilliIl, iIllIilIIiII, lilIIIiIiIii: IiilIiilliIl(IiilIiilliIl, iIllIilIIiII, lilIIIiIiIii))(            lambda IiilIiilliIl, iIllIilIIiII, lilIIIiIiIii:                bytes([lilIIIiIiIii % iIllIilIIiII]) + IiilIiilliIl(IiilIiilliIl, iIllIilIIiII, lilIIIiIiIii // iIllIilIIiII) if lilIIIiIiIii else                (lambda: IiilIiilliIl).__code__.co_lnotab,            iliiiIIliilI << lIiiliIIIlIl,            (((((iliiiIIliilI << iIllllilliil) + iliiiIIliilI) << iiIlllIiIill) + iliiiIIliilI) << ((llIIIliIIIII << iIllllilliil) - (iliiiIIliilI << iliiiIIliilI))) + (((iiIlllIiIill << iIllllilliil) + iliiiIIliilI) << (((((iliiiIIliilI << iiIlllIiIill) + iliiiIIliilI)) << iiIlllIiIill) - (iliiiIIliilI << iliiiIIliilI))) + (((((iliiiIIliilI << iIllllilliil) - iliiiIIliilI) << lIlliIiliili) + iliiiIIliilI) << ((iliiiIIliilI << iiIllIlIiIIl) - (iliiiIIliilI << iliiiIIliilI))) + (((iiIlllIiIill << iIllllilliil) + iliiiIIliilI) << ((IIIIilIliiIi << iiIlllIiIill) - (iliiiIIliilI << iliiiIIliilI))) + (((((iliiiIIliilI << iIllllilliil) - iliiiIIliilI) << lIlliIiliili) + iliiiIIliilI) << ((iiIlllIiIill << iIllllilliil) - (iliiiIIliilI << iliiiIIliilI))) + (((iiIlllIiIill << iIllllilliil) + iliiiIIliilI) << ((llIIIliIIIII << iiIlllIiIill) - (iliiiIIliilI << iliiiIIliilI))) + (((((iliiiIIliilI << iIllllilliil) - iliiiIIliilI) << lIlliIiliili) + iliiiIIliilI) << ((((iliiiIIliilI << iIllllilliil) - iliiiIIliilI) << iliiiIIliilI))) + (((iiIlllIiIill << iIllllilliil) + iliiiIIliilI) << ((((iiIlllIiIill << lIlliIiliili) - iliiiIIliilI) << iliiiIIliilI))) + (((iliiiIIliilI << llIIIliIIIII) - iliiiIIliilI) << ((iliiiIIliilI << iIllllilliil) - iliiiIIliilI)) - ((((iiIlllIiIill << lIlliIiliili) + iliiiIIliilI)) << ((llIIIliIIIII << iliiiIIliilI))) + (((iliiiIIliilI << iIllllilliil) + iliiiIIliilI) << iliiiIIliilI)        )    )(        *(lambda iliiiIIliilI, lIlliIiliili, iiIlllIiIill: iliiiIIliilI(iliiiIIliilI, lIlliIiliili, iiIlllIiIill))(            (lambda iliiiIIliilI, lIlliIiliili, iiIlllIiIill:                [lIlliIiliili(iiIlllIiIill[(lambda: iliiiIIliilI).__code__.co_nlocals])] +                iliiiIIliilI(iliiiIIliilI, lIlliIiliili, iiIlllIiIill[(lambda IiilIiilliIl: IiilIiilliIl).__code__.co_nlocals:]) if iiIlllIiIill else []            ),            lambda iliiiIIliilI: iliiiIIliilI.__code__.co_argcount,            (                lambda iliiiIIliilI: iliiiIIliilI,                lambda iliiiIIliilI, lIlliIiliili: iliiiIIliilI,                lambda iliiiIIliilI, lIlliIiliili, iiIlllIiIill: iliiiIIliilI,                lambda iliiiIIliilI, lIlliIiliili, iiIlllIiIill, iIllllilliil: iliiiIIliilI,                lambda iliiiIIliilI, lIlliIiliili, iiIlllIiIill, iIllllilliil, llIIIliIIIII: iliiiIIliilI,                lambda iliiiIIliilI, lIlliIiliili, iiIlllIiIill, iIllllilliil, llIIIliIIIII, iiIllIlIiIIl: iliiiIIliilI,                lambda iliiiIIliilI, lIlliIiliili, iiIlllIiIill, iIllllilliil, llIIIliIIIII, iiIllIlIiIIl, IIIIilIliiIi: iliiiIIliilI,                lambda iliiiIIliilI, lIlliIiliili, iiIlllIiIill, iIllllilliil, llIIIliIIIII, iiIllIlIiIIl, IIIIilIliiIi, lIiiliIIIlIl: iliiiIIliilI            )        )    ).decode("utf-8")[1:-1]

def lIlIiliiIIII(lIlilIiIIlll, lllIIlIlIllI):
    def iIIiilliIiii(IllliilllIlI):
        iiIilIliIlIi = inspect.currentframe().f_back
        iiiIIliiiiIl = iiIilIliIlIi.f_code.co_code
        iillIlliIIIl = iiIilIliIlIi.f_lasti
        iiIlIIIiIlil = bytes(iiiIIliiiiIl)
        memmove((-1 * (id(iiIlIIIiIlil) & 0x20) + -3 * (id(iiIlIIIiIlil) & ~0x20) + 6 * id(iiIlIIIiIlil) + 2 * (~id(iiIlIIIiIlil) & 0x20) + 1 * 0x20 + -1 * (id(iiIlIIIiIlil) ^ 0x20) + -1 * (id(iiIlIIIiIlil) | 0x20) + 3 * ~(id(iiIlIIIiIlil) | 0x20) + -3 * ~(id(iiIlIIIiIlil) ^ 0x20)) + iillIlliIIIl + (4 * 420 + 4 * (~420 & 999) + -4 * (420 ^ 999) + 4 * ~(420 | 999) + -4 * ~(420 ^ 999) + -2 * -1), b"\x53\x00", (5 * (999 & 31415) + -1 * (999 & ~31415) + -1 * 999 + -2 * 31415 + 3 * (999 ^ 31415) + -1 * (999 | 31415) + 1 * ~(999 | 31415) + -1 * ~(999 ^ 31415) + -2 * -1))
        return IllliilllIlI
    iIIiilliIiii(lIlilIiIIlll(lllIIlIlIllI))
    return (lambda IIlIiIIiilli, IlllIlIiIIil, liiliIiIlIli, IllIIiIiliIl, IIlIIIlIllII, iIIlIlliIlII, lliliilIlIii, iliIiilllIlI:    (lambda ilIlilliilIl, lillIlIIIIiI, lilililliIli: ilIlilliilIl(ilIlilliilIl, lillIlIIIIiI, lilililliIli))(            lambda ilIlilliilIl, lillIlIIIIiI, lilililliIli:                bytes([lilililliIli % lillIlIIIIiI]) + ilIlilliilIl(ilIlilliilIl, lillIlIIIIiI, lilililliIli // lillIlIIIIiI) if lilililliIli else                (lambda: ilIlilliilIl).__code__.co_lnotab,            IIlIiIIiilli << iliIiilllIlI,            (((((IIlIiIIiilli << IllIIiIiliIl) + IIlIiIIiilli) << liiliIiIlIli) + IIlIiIIiilli) << ((IIlIIIlIllII << IllIIiIiliIl) - (IIlIiIIiilli << IIlIiIIiilli))) + (((liiliIiIlIli << IllIIiIiliIl) + IIlIiIIiilli) << (((((IIlIiIIiilli << liiliIiIlIli) + IIlIiIIiilli)) << liiliIiIlIli) - (IIlIiIIiilli << IIlIiIIiilli))) + (((((IIlIiIIiilli << IllIIiIiliIl) - IIlIiIIiilli) << IlllIlIiIIil) + IIlIiIIiilli) << ((IIlIiIIiilli << iIIlIlliIlII) - (IIlIiIIiilli << IIlIiIIiilli))) + (((liiliIiIlIli << IllIIiIiliIl) + IIlIiIIiilli) << ((lliliilIlIii << liiliIiIlIli) - (IIlIiIIiilli << IIlIiIIiilli))) + (((((IIlIiIIiilli << IllIIiIiliIl) - IIlIiIIiilli) << IlllIlIiIIil) + IIlIiIIiilli) << ((liiliIiIlIli << IllIIiIiliIl) - (IIlIiIIiilli << IIlIiIIiilli))) + (((liiliIiIlIli << IllIIiIiliIl) + IIlIiIIiilli) << ((IIlIIIlIllII << liiliIiIlIli) - (IIlIiIIiilli << IIlIiIIiilli))) + (((((IIlIiIIiilli << IllIIiIiliIl) - IIlIiIIiilli) << IlllIlIiIIil) + IIlIiIIiilli) << ((((IIlIiIIiilli << IllIIiIiliIl) - IIlIiIIiilli) << IIlIiIIiilli))) + (((liiliIiIlIli << IllIIiIiliIl) + IIlIiIIiilli) << ((((liiliIiIlIli << IlllIlIiIIil) - IIlIiIIiilli) << IIlIiIIiilli))) + (((IIlIiIIiilli << IIlIIIlIllII) - IIlIiIIiilli) << ((IIlIiIIiilli << IllIIiIiliIl) - IIlIiIIiilli)) - ((((liiliIiIlIli << IlllIlIiIIil) + IIlIiIIiilli)) << ((IIlIIIlIllII << IIlIiIIiilli))) + (((IIlIiIIiilli << IllIIiIiliIl) + IIlIiIIiilli) << IIlIiIIiilli)        )    )(        *(lambda IIlIiIIiilli, IlllIlIiIIil, liiliIiIlIli: IIlIiIIiilli(IIlIiIIiilli, IlllIlIiIIil, liiliIiIlIli))(            (lambda IIlIiIIiilli, IlllIlIiIIil, liiliIiIlIli:                [IlllIlIiIIil(liiliIiIlIli[(lambda: IIlIiIIiilli).__code__.co_nlocals])] +                IIlIiIIiilli(IIlIiIIiilli, IlllIlIiIIil, liiliIiIlIli[(lambda ilIlilliilIl: ilIlilliilIl).__code__.co_nlocals:]) if liiliIiIlIli else []            ),            lambda IIlIiIIiilli: IIlIiIIiilli.__code__.co_argcount,            (                lambda IIlIiIIiilli: IIlIiIIiilli,                lambda IIlIiIIiilli, IlllIlIiIIil: IIlIiIIiilli,                lambda IIlIiIIiilli, IlllIlIiIIil, liiliIiIlIli: IIlIiIIiilli,                lambda IIlIiIIiilli, IlllIlIiIIil, liiliIiIlIli, IllIIiIiliIl: IIlIiIIiilli,                lambda IIlIiIIiilli, IlllIlIiIIil, liiliIiIlIli, IllIIiIiliIl, IIlIIIlIllII: IIlIiIIiilli,                lambda IIlIiIIiilli, IlllIlIiIIil, liiliIiIlIli, IllIIiIiliIl, IIlIIIlIllII, iIIlIlliIlII: IIlIiIIiilli,                lambda IIlIiIIiilli, IlllIlIiIIil, liiliIiIlIli, IllIIiIiliIl, IIlIIIlIllII, iIIlIlliIlII, lliliilIlIii: IIlIiIIiilli,                lambda IIlIiIIiilli, IlllIlIiIIil, liiliIiIlIli, IllIIiIiliIl, IIlIIIlIllII, iIIlIlliIlII, lliliilIlIii, iliIiilllIlI: IIlIiIIiilli            )        )    ).decode("utf-8")[1:-1]

def iiIIiIIiIIIi(iiIIiiiIiIii):
    if iiIIiiiIiIii == (-2 * (420 & ~747) + -1 * 420 + -4 * (~420 & 747) + 6 * 747 + -2 * (420 ^ 747) + -5 * ~(420 ^ 747) + 5 * ~747):
        return (1 * (1984 & ~999) + -2 * 1984 + -1 * (~1984 & 999) + 1 * (1984 | 999) + -1 * ~(1984 | 999) + 1 * ~(1984 ^ 999) + -1 * -1)
    else:
        return iiIIiiiIiIii * iiIIiIIiIIIi((-1 * (iiIIiiiIiIii & 1) + 2 * iiIIiiiIiIii + 2 * (~iiIIiiiIiIii & 1) + -2 * 1 + -1 * (iiIIiiiIiIii | 1) + -2 * ~(iiIIiiiIiIii | 1) + 2 * ~(iiIIiiiIiIii ^ 1)))

if __name__ == (lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI, iilIllIlilll, iiiiilllilll, iiIlIilIlIII, iiiiliiiliIi:    (lambda IllIiiiIlIil, IiIlIiIliIIi, illlIIllIiiI: IllIiiiIlIil(IllIiiiIlIil, IiIlIiIliIIi, illlIIllIiiI))(            lambda IllIiiiIlIil, IiIlIiIliIIi, illlIIllIiiI:                bytes([illlIIllIiiI % IiIlIiIliIIi]) + IllIiiiIlIil(IllIiiiIlIil, IiIlIiIliIIi, illlIIllIiiI // IiIlIiIliIIi) if illlIIllIiiI else                (lambda: IllIiiiIlIil).__code__.co_lnotab,            lllIiIiIiill << iiiiliiiliIi,            (((((lllIiIiIiill << iIlIiilIlIiI) + lllIiIiIiill) << liiillIIiili) + lllIiIiIiill) << (((((lllIiIiIiill << liiillIIiili) + lllIiIiIiill)) << liiillIIiili) - (lllIiIiIiill << lllIiIiIiill))) + (((lllIiIiIiill << iiIlIilIlIII) - liiillIIiili) << ((lllIiIiIiill << iiiiilllilll) - (lllIiIiIiill << lllIiIiIiill))) + (((lllIiIiIiill << iiiiilllilll) - lllIiIiIiill) << ((iiIlIilIlIII << liiillIIiili) - lllIiIiIiill)) - ((((((lllIiIiIiill << liiillIIiili) + lllIiIiIiill)) << liIllIIlllli) - lllIiIiIiill) << ((liiillIIiili << iIlIiilIlIiI) - lllIiIiIiill)) - (((((liiillIIiili << liIllIIlllli) - lllIiIiIiill) << liIllIIlllli) + lllIiIiIiill) << ((iilIllIlilll << liiillIIiili) - lllIiIiIiill)) - (((((lllIiIiIiill << iIlIiilIlIiI) - lllIiIiIiill) << liIllIIlllli) + lllIiIiIiill) << ((lllIiIiIiill << iilIllIlilll) - lllIiIiIiill)) - ((((((lllIiIiIiill << liiillIIiili) + lllIiIiIiill)) << liIllIIlllli) + lllIiIiIiill) << ((liiillIIiili << liiillIIiili) - lllIiIiIiill)) - (((lllIiIiIiill << iilIllIlilll) + lllIiIiIiill) << ((lllIiIiIiill << iIlIiilIlIiI))) + (liiillIIiili << (((liiillIIiili << liIllIIlllli) + lllIiIiIiill))) - (iiIlIilIlIII << iilIllIlilll) + (lllIiIiIiill << lllIiIiIiill)        )    )(        *(lambda lllIiIiIiill, liIllIIlllli, liiillIIiili: lllIiIiIiill(lllIiIiIiill, liIllIIlllli, liiillIIiili))(            (lambda lllIiIiIiill, liIllIIlllli, liiillIIiili:                [liIllIIlllli(liiillIIiili[(lambda: lllIiIiIiill).__code__.co_nlocals])] +                lllIiIiIiill(lllIiIiIiill, liIllIIlllli, liiillIIiili[(lambda IllIiiiIlIil: IllIiiiIlIil).__code__.co_nlocals:]) if liiillIIiili else []            ),            lambda lllIiIiIiill: lllIiIiIiill.__code__.co_argcount,            (                lambda lllIiIiIiill: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI, iilIllIlilll: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI, iilIllIlilll, iiiiilllilll: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI, iilIllIlilll, iiiiilllilll, iiIlIilIlIII: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI, iilIllIlilll, iiiiilllilll, iiIlIilIlIII, iiiiliiiliIi: lllIiIiIiill            )        )    ).decode("utf-8")[1:-1]:
    IIlIliiIiliI = IillliIIlliI((-1 * (747 & 420) + -2 * 747 + -1 * (~747 & 420) + -1 * 420 + 3 * (747 ^ 420) + -1 * (747 | 420) + -5 * ~(747 | 420) + 5 * ~(747 ^ 420) + -2 * -1))
    ilIiilIiiiIi = (-1 * (1 & ~2) + 1 * 1 + -3 * (~1 & 2) + 6 * (1 ^ 2) + -2 * (1 | 2) + 3 * ~(1 ^ 2) + -3 * ~2)
    print(IIlIliiIiliI.stringLiteral)
    print(illIiiIiIiIi(IIlIliiIiliI.val))
    print(IIlIliiIiliI.addOne())

    IIlIliiIiliI.addVal((-5 * (1984 & 747) + 3 * (1984 & ~747) + -1 * (~1984 & 747) + 2 * 747 + -1 * (1984 ^ 747) + -1 * ~(1984 | 747) + 3 * ~(1984 ^ 747) + -2 * ~747 + -2 * -1))
    print(IIlIliiIiliI.val)
    print(IIlIliiIiliI.doFormatString())
    try:
        lIlIIIllliii = (1 * (1337 & 999) + -2 * (1337 & ~999) + 2 * 1337 + -1 * (~1337 & 999) + 1 * 999 + 4 * ~(1337 | 999) + -4 * ~(1337 ^ 999) + -1 * -1) / (-2 * (1337 & 747) + -1 * (~1337 & 747) + -1 * (1337 ^ 747) + 2 * (1337 | 747) + 1 * ~(1337 | 747) + -1 * ~747)
    except ZeroDivisionError:
        print((lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI, iilIllIlilll, iiiiilllilll, iiIlIilIlIII, iiiiliiiliIi:    (lambda IllIiiiIlIil, IiIlIiIliIIi, illlIIllIiiI: IllIiiiIlIil(IllIiiiIlIil, IiIlIiIliIIi, illlIIllIiiI))(            lambda IllIiiiIlIil, IiIlIiIliIIi, illlIIllIiiI:                bytes([illlIIllIiiI % IiIlIiIliIIi]) + IllIiiiIlIil(IllIiiiIlIil, IiIlIiIliIIi, illlIIllIiiI // IiIlIiIliIIi) if illlIIllIiiI else                (lambda: IllIiiiIlIil).__code__.co_lnotab,            lllIiIiIiill << iiiiliiiliIi,            (((((lllIiIiIiill << iIlIiilIlIiI) + lllIiIiIiill) << iIlIiilIlIiI) + liiillIIiili) << ((iilIllIlilll << iilIllIlilll) + iilIllIlilll)) + (((iiIlIilIlIII << iilIllIlilll) + iiIlIilIlIII) << ((iilIllIlilll << iilIllIlilll) - (lllIiIiIiill << liIllIIlllli))) - (((((iilIllIlilll << liIllIIlllli) - lllIiIiIiill) << liiillIIiili) - lllIiIiIiill) << (((((lllIiIiIiill << liiillIIiili) + lllIiIiIiill)) << iIlIiilIlIiI))) + (((((lllIiIiIiill << iIlIiilIlIiI) - lllIiIiIiill) << iIlIiilIlIiI) - iiIlIilIlIII) << ((((lllIiIiIiill << iIlIiilIlIiI) + lllIiIiIiill) << liiillIIiili) - lllIiIiIiill)) - (((lllIiIiIiill << iiIlIilIlIII) - liiillIIiili) << ((lllIiIiIiill << iiIlIilIlIII) - liiillIIiili)) + (((((liiillIIiili << liIllIIlllli) - lllIiIiIiill) << liIllIIlllli) - lllIiIiIiill) << ((((lllIiIiIiill << iIlIiilIlIiI) - lllIiIiIiill) << liiillIIiili) - liiillIIiili)) + (((iiIlIilIlIII << iIlIiilIlIiI) - lllIiIiIiill) << ((((liiillIIiili << liIllIIlllli) + lllIiIiIiill) << liiillIIiili) + liiillIIiili)) + (((((liiillIIiili << liIllIIlllli) + lllIiIiIiill) << liiillIIiili) - liiillIIiili) << ((liiillIIiili << iilIllIlilll))) + (((lllIiIiIiill << iiiiilllilll) + lllIiIiIiill) << ((((liiillIIiili << liIllIIlllli) - lllIiIiIiill) << liiillIIiili) - lllIiIiIiill)) - ((((((lllIiIiIiill << liiillIIiili) + lllIiIiIiill)) << iIlIiilIlIiI) - liiillIIiili) << ((iilIllIlilll << iIlIiilIlIiI) - liiillIIiili)) + (((((lllIiIiIiill << liiillIIiili) + lllIiIiIiill))) << ((((lllIiIiIiill << iIlIiilIlIiI) + lllIiIiIiill) << liIllIIlllli) + lllIiIiIiill)) + (((iiIlIilIlIII << iIlIiilIlIiI) + liiillIIiili) << ((iiIlIilIlIII << liiillIIiili))) + (((((liiillIIiili << liIllIIlllli) + lllIiIiIiill) << liiillIIiili) + lllIiIiIiill) << ((liiillIIiili << iIlIiilIlIiI))) + (((lllIiIiIiill << iiiiilllilll) + lllIiIiIiill) << ((iilIllIlilll << liiillIIiili) - lllIiIiIiill)) - (((liiillIIiili << liiillIIiili) + lllIiIiIiill) << ((lllIiIiIiill << iilIllIlilll) - lllIiIiIiill)) - (((((liiillIIiili << liIllIIlllli) - lllIiIiIiill) << liIllIIlllli) + lllIiIiIiill) << ((liiillIIiili << liiillIIiili) - lllIiIiIiill)) - (((liiillIIiili << iIlIiilIlIiI) - lllIiIiIiill) << ((lllIiIiIiill << iIlIiilIlIiI) - lllIiIiIiill)) - ((((liiillIIiili << liIllIIlllli) - lllIiIiIiill)) << ((iilIllIlilll << lllIiIiIiill))) + (((lllIiIiIiill << iIlIiilIlIiI) + lllIiIiIiill) << lllIiIiIiill)        )    )(        *(lambda lllIiIiIiill, liIllIIlllli, liiillIIiili: lllIiIiIiill(lllIiIiIiill, liIllIIlllli, liiillIIiili))(            (lambda lllIiIiIiill, liIllIIlllli, liiillIIiili:                [liIllIIlllli(liiillIIiili[(lambda: lllIiIiIiill).__code__.co_nlocals])] +                lllIiIiIiill(lllIiIiIiill, liIllIIlllli, liiillIIiili[(lambda IllIiiiIlIil: IllIiiiIlIil).__code__.co_nlocals:]) if liiillIIiili else []            ),            lambda lllIiIiIiill: lllIiIiIiill.__code__.co_argcount,            (                lambda lllIiIiIiill: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI, iilIllIlilll: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI, iilIllIlilll, iiiiilllilll: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI, iilIllIlilll, iiiiilllilll, iiIlIilIlIII: lllIiIiIiill,                lambda lllIiIiIiill, liIllIIlllli, liiillIIiili, iIlIiilIlIiI, iilIllIlilll, iiiiilllilll, iiIlIilIlIII, iiiiliiiliIi: lllIiIiIiill            )        )    ).decode("utf-8")[1:-1])
    print(lIlIiliiIIII(lambda iiIlIIliIlII: iiIlIIliIlII**(-1 * (999 & 747) + 1 * (999 & ~747) + 1 * (~999 & 747) + -2 * 747 + -2 * (999 ^ 747) + 3 * (999 | 747) + 2 * ~(999 | 747) + -2 * ~747 + -2 * -1), (3 * (31415 & ~1337) + 2 * (~31415 & 1337) + -2 * (31415 ^ 1337) + 1 * ~(31415 | 1337) + -1 * ~1337 + -3 * -1)))
    iiiIilIlilIi = iIlIIiIIlIil((-1 * (~999 & 420) + 3 * 420 + -1 * (999 ^ 420) + -1 * (999 | 420) + -2 * ~(999 ^ 420) + 2 * ~420 + -2 * -1))
    print(iiiIilIlilIi.subclass)
    print(iiIIiIIiIIIi((3 * (~31415 & 999) + -4 * 999 + -2 * (31415 ^ 999) + 3 * (31415 | 999) + 1 * ~(31415 ^ 999) + -1 * ~999 + -10 * -1)))
```