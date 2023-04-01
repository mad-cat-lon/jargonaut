# unicloak ![pep-8](https://github.com/xor-eax-eax-ret/unicloak/actions/workflows/pep8.yml/badge.svg)
Unicode support can make things weird sometimes, especially when code is involved. `unicloak` abuses identifier normalization in Python, making code still somewhat readable but possibly bypassing human inspection or string-based matching defenses by replacing everything with an equivalent identifier variant. I wrote this after seeing a [writeup](https://blog.phylum.io/malicious-actors-use-unicode-support-in-python-to-evade-detection) on a malicious Python package that uses this same method to evade AV detection.
NOTE: I plan on turning this into a fully-featured Python obfuscator like [pyminifier](https://github.com/liftoff/pyminifier) soon. 

## Usage
```unicloak.py file_to_obfuscate.py obfuscated.py```

## Example output
```
import math as 𝘮a𝘵𝓱
class 𝕾ｑ𝙪𝑎𝙧𝚎:
    def __init__(self, val):
        𝒔𝗲𝗹𝙛.val = 𝙫𝒶ˡ
    def 𝚖ａ𝓉𝓱﹎𝔰𝓆𝚛𝘵(self):
        return 𝙢ᵃ𝘁𝙝.sqrt(ｓᵉⅼ𝑓.val)
    def ｍ𝘢ｔ𝓱︳𝕤𝘲𝚞𝖆𝒓e(self):
        return 𝒎𝙖𝒕𝙝.pow(𝑠𝙚𝖑𝕗.val, 2)
    def ſ𝘲𝐮𝒶𝙧𝖊(self):
        return 𝚜ⅇ𝚕𝕗.val ** 2

def 𝗺𝖺𝔦𝔫():
    𝗌𝚚 = 𝙎𝚚𝖚ᵃ𝗋𝑒(2)
    print(𝘀𝗾.math_sqrt())
    print(s𝓺.math_square())
    print(sｑ.square())
   
if __name__ == '__main__':
    𝘮ₐ𝔦𝑛()
```
## References
- https://blog.phylum.io/malicious-actors-use-unicode-support-in-python-to-evade-detection
- https://peps.python.org/pep-0672/#normalizing-identifiers
- https://peps.python.org/pep-3131/
- https://unicode.org/reports/tr15/
- https://docs.python.org/3/library/ast.html
