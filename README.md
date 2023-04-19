# unicloak ![pep-8](https://github.com/xor-eax-eax-ret/unicloak/actions/workflows/pep8.yml/badge.svg)
`unicloak` is an obfuscator for hiding and protecting Python code with a few novel features. Note that this is a work in progress! 

## Features
- Evade string matching with [Unicode identifier variants](https://blog.phylum.io/malicious-actors-use-unicode-support-in-python-to-evade-detection). 
- [Linear mixed boolean arithmetic expressions](https://link.springer.com/chapter/10.1007/978-3-540-77535-5_5)

## Upcoming features 
- Logging / debugging 
- Obfuscate based on user-defined rules 
- String obfuscation methods 
- Dead code insertion
- Variable obfuscation methods (e.g `useful_var_name` -> `1l1l1l1lll`)
- Comment removal 
- Dead parameter insertion
- Type hint removal 
- C function conversion a la [pyarmor](https://github.com/dashingsoft/pyarmor)
- Documentation
- Better performance (maybe don't use z3 for MBA)

## Usage
```main.py source.py obfuscated.py```

## Examples
### Unicode identifier variants
#### Original
```
import math
import requests
from win32crypt import CryptUnprotectData

if __name__ == "__main__":
    external_ip = requests.get('http://whatismyip.akamai.com/').text
    CryptUnprotectData(b"foobar")
    print(external_ip)
```
#### Obfuscated 
```
import ₘₐ𝖙𝗁
import ｒ𝖊𝚚𝒖𝚎ſ𝘁ˢ
from 𝙬ᵢ𝔫３𝟐ｃ𝓻𝗒𝔭𝑡 import 𝕮𝓇𝘆𝖕𝔱𝒰𝗻𝒑𝑟𝗼𝓉𝗲ⅽ𝖙Ⅾ𝙖𝑡ᵃ
if __name__ == '__main__':
    𝘦𝔁𝑡ₑᵣ𝖓𝚊𝖑＿𝗂ｐ = 𝓇ℯ𝚚ᵤℯ𝐬𝘁s.get('http://whatismyip.akamai.com/').text
    Ｃ𝗋y𝒑𝒕𝕌ₙ𝘱𝘳𝑜𝔱ⅇ𝖼𝙩𝒟𝒶𝙩𝙖(b'foobar')
    print(𝖾𝚡ᵗ𝐞𝗿𝚗aℓ︴𝓲𝘱)
```
### MBA obfuscation
#### Original 
```
def op(x):
    a = 1
    b = 2
    c = a + b
    d = x - c 
    return d + 10

if __name__ == "__main__":
    a = op(10)
    print(a)
```
#### Obfuscated 
```
def op(x):
    a = -1 * (1337 & ~1984) + 1 * 1337 + 1 * (1337 ^ 1984) + -1 * (1337 | 1984) + -1 * -1
    b = -1 * (1337 & 1984) + -1 * (1337 & ~1984) + -1 * (~1337 & 1984) + 1 * (1337 ^ 1984) + -1 * ~(1337 | 1984) + 1 * ~(1337 ^ 1984) + -2 * -1
    c = -(-1 * (1337 & 1984) + -1 * (1337 & ~1984) + -1 * 1984 + 1 * (1337 | 1984) + -1 * ~(1337 | 1984) + 1 * ~(1337 ^ 1984) + -5 * -1) * (a & b) + (-1 * (~1337 & 1984) + -2 * 1984 + 5 * (1337 ^ 1984) + -2 * (1337 | 1984) + -1 * ~(1337 | 1984) + 4 * ~(1337 ^ 1984) + -3 * ~1984 + -1 * -1) * a + -(1 * (1337 & 1984) + -2 * (1337 & ~1984) + -1 * (~1337 & 1984) + 2 * 1984 + -1 * (1337 ^ 1984) + -3 * ~(1337 ^ 1984) + 3 * ~1984 + -1 * -1) * b + -(1 * 1984 + -1 * (1337 | 1984) + -1 * ~(1337 | 1984) + 1 * ~1984 + -1 * -1) * (a ^ b) + (2 * (1337 & 1984) + 1 * (~1337 & 1984) + -1 * 1984 + 1 * (1337 ^ 1984) + -1 * (1337 | 1984) + -3 * -1) * (a | b) + -(1 * (1337 & 1984) + -2 * 1337 + -3 * 1984 + 3 * (1337 | 1984) + 1 * ~(1337 ^ 1984) + -1 * ~1984 + -2 * -1) * ~(a | b) + (5 * (1337 & ~1984) + -3 * 1337 + -1 * ~(1337 | 1984) + 3 * ~(1337 ^ 1984) + -2 * ~1984 + -4 * -1) * ~(a ^ b) + -(2 * (1337 & 1984) + 2 * (~1337 & 1984) + -2 * 1984 + -2 * -1) * ~b
    d = (2 * (1337 & 1984) + 2 * (1337 & ~1984) + 2 * (~1337 & 1984) + -1 * 1984 + -1 * (1337 | 1984) + 1 * ~(1337 | 1984) + -1 * ~1984 + -3 * -1) * x + (2 * (1337 & 1984) + 2 * 1337 + 2 * (~1337 & 1984) + -2 * (1337 | 1984) + 2 * ~(1337 | 1984) + -2 * ~(1337 ^ 1984) + -3 * -1) * (~x & c) + -(-2 * (1337 & ~1984) + -4 * (~1337 & 1984) + 8 * (1337 ^ 1984) + -4 * (1337 | 1984) + -2 * ~(1337 | 1984) + 4 * ~(1337 ^ 1984) + -2 * ~1984 + -3 * -1) * c + -(3 * (1337 & 1984) + -4 * (1337 & ~1984) + -1 * (~1337 & 1984) + -1 * 1984 + 2 * (1337 ^ 1984) + -2 * ~(1337 ^ 1984) + 2 * ~1984 + -1 * -1) * (x ^ c) + (-1 * (1337 & 1984) + -2 * (1337 & ~1984) + 2 * 1337 + 2 * (~1337 & 1984) + -1 * 1984 + -1 * (1337 ^ 1984) + -1 * ~(1337 | 1984) + 1 * ~1984 + -1 * -1) * ~(x | c) + -(-2 * (1337 & 1984) + -1 * 1337 + -4 * (~1337 & 1984) + 5 * 1984 + -1 * (1337 | 1984) + -1 * ~(1337 | 1984) + -1 * ~(1337 ^ 1984) + 2 * ~1984 + -1 * -1) * ~c
    return d + (-4 * (1337 & 1984) + 1 * 1337 + -1 * (~1337 & 1984) + 1 * 1984 + -1 * ~(1337 | 1984) + 2 * ~(1337 ^ 1984) + -1 * ~1984 + -10 * -1)
if __name__ == '__main__':
    a = op(1 * (1337 & 1984) + 1 * (1337 ^ 1984) + -1 * (1337 | 1984) + -10 * -1)
    print(a)
```
## Requirements 
z3-solver
numpy

## References
- https://blog.phylum.io/malicious-actors-use-unicode-support-in-python-to-evade-detection
- https://peps.python.org/pep-0672/#normalizing-identifiers
- https://peps.python.org/pep-3131/
- https://unicode.org/reports/tr15/
- https://docs.python.org/3/library/ast.html
- https://link.springer.com/chapter/10.1007/978-3-540-77535-5_5
- https://theses.hal.science/tel-01623849/document
- https://bbs.kanxue.com/thread-271574.htm