import libcst as cst
import random


class BinaryString(cst.CSTTransformer):
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

    def visit_Call(self, node: cst.Call):
        # This implementation breaks open(filename, mode) so we avoid it 
        if isinstance(node.func, cst.Name):
            if node.func.value == "open":
                return False
        
    def leave_SimpleString(
        self, 
        original_node: cst.SimpleString,
        updated_node: cst.SimpleString
    ):
        if len(original_node.value) > 3:
            string_as_bin = self._text_to_bits(original_node.value)
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            vars = [
                ''.join(random.choice(alphabet.upper() + alphabet.lower()) for i in range(5)) 
                for j in range(5)
            ]
            obfus = ''.join(self.keys[0] if i == "0" else self.keys[1] for i in string_as_bin)
            # TODO: Change from f-string to actual code to prevent AttributeError
            decode_func = f"(lambda {vars[0]}, {vars[1]}=\"utf-8\", {vars[2]}=\"surrogatepass\": \
                (({vars[3]} := int({vars[0]}, 2))).to_bytes(({vars[3]}.bit_length() + 7)\
                // 8, \"big\").decode({vars[1]}, {vars[2]}) or \"\")"
            to_bin_func = f"(\"\".join([\"0\" if {vars[4]} == \"{self.keys[0]}\" else \"1\"\
                for {vars[4]} in \"{obfus}\"]))"
            result = decode_func + to_bin_func
            result = cst.parse_expression(result)
            return result
        return original_node