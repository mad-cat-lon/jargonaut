# unicloak 
Unicode support can make things weird sometimes, especially when code is involved. `unicloak` abuses identifier normalization in Python, making code still somewhat readable but possibly bypassing human inspection or string-based matching defenses by replacing everything with an equivalent identifier variant. I wrote this after seeing a [writeup](https://blog.phylum.io/malicious-actors-use-unicode-support-in-python-to-evade-detection) on a malicious Python package that uses this same method to evade AV detection.
NOTE: I plan on turning this into a fully-featured Python obfuscator like [pyminifier](https://github.com/liftoff/pyminifier) soon. 

## usage
```unicloak.py file_to_obfuscate.py obfuscated.py```

## References
- https://blog.phylum.io/malicious-actors-use-unicode-support-in-python-to-evade-detection
- https://peps.python.org/pep-0672/#normalizing-identifiers
- https://peps.python.org/pep-3131/
- https://unicode.org/reports/tr15/
- https://docs.python.org/3/library/ast.html