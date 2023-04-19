import ast 
import random 


def _text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def binary(keys, string):
    """
    Obfuscates string literals by encoding them as binary and then
    using similar-looking Unicode characters to represent the 1s and 0s
    """
    if len(keys) != 2:
        raise Exception(
            "Must provide 2 characters for binary string obfuscation."
        )
    string_as_bin = _text_to_bits(string)
    # Generate random variable names for the lambda functions 
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    vars = [
        ''.join(random.choice(alphabet.upper() + alphabet.lower()) for i in range(5)) 
        for j in range(5)
    ]
    obfus = ''.join([keys[0] if i == "0" else keys[1] for i in string_as_bin])
    decode_func = "(lambda b, e='utf-8', err='surrogatepass': ((n := int(b, 2))).to_bytes((\
            n.bit_length() + 7) // 8, 'big').decode(e, err) or '')"
    decode_func = f"(lambda {vars[0]}, {vars[1]}='utf-8', {vars[2]}='surrogatepass':\
        (({vars[3]} := int({vars[0]}, 2))).to_bytes(({vars[3]}.bit_length() + 7) // 8, 'big')\
        .decode({vars[1]}, {vars[2]}) or '')"
    to_bin_func = f"(''.join(['0' if {vars[4]} == '{keys[0]}' else '1'\
        for {vars[4]} in '{obfus}']))"
    final_expr = decode_func + to_bin_func
    final_expr = ast.parse(final_expr).body[0]
    return final_expr
