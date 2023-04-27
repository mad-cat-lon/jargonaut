import ast 
import random


class BinaryString(ast.NodeTransformer):
    """
    Obfuscates string literals by encoding them as binary and then
    using similar-looking Unicode characters to represent the 1s and 0s.
    """
    def __init__(self, avoid=None, keys=["Ꭓ", "𝑿", "𝙓", "𝚇"]):
        self.avoid = avoid
        self.keys = random.sample(keys, 2)

    def _text_to_bits(self, text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, str):
            print(node.value)
            string_as_bin = self._text_to_bits(node.value)
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            vars = [
                ''.join(random.choice(alphabet.upper() + alphabet.lower()) for i in range(5)) 
                for j in range(5)
            ]
            obfus = ''.join(self.keys[0] if i == "0" else self.keys[1] for i in string_as_bin)
            decode_func = f"(lambda {vars[0]}, {vars[1]}='utf-8', {vars[2]}='surrogatepass':\
                (({vars[3]} := int({vars[0]}, 2))).to_bytes(({vars[3]}.bit_length() + 7) // 8, 'big')\
                .decode({vars[1]}, {vars[2]}) or '')"
            to_bin_func = f"(''.join(['0' if {vars[4]} == '{self.keys[0]}' else '1'\
                for {vars[4]} in '{obfus}']))"
            final_expr = decode_func + to_bin_func
            final_expr = ast.parse(final_expr).body[0]
            return final_expr.value
        return node