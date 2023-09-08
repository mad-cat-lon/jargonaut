# Maps python bytecode instruction to our own instruction set
# Each python opcode can map to multiple opcodes on our end - we can randomize it per obfuscation pass
# Including human-readable names for debugging purposes

# Format:
# op arg next_handler (encoded)
# Not having an explicit handler table is really great for obfuscation 
# For now, VM opcode names will be same as in Python 

OPCODE_MAP = {
    # General instructions 
    "NOP": [
        ("NOP", 0)
    ],
    "POP_TOP": [
        ("POP_TOP", 1)
    ],
    "ROT_TWO": [
        ("ROT_TWO", 2)
    ],
    "ROT_THREE": [
        ("ROT_THREE", 3)
    ],
    "DUP_TOP": [
        ("DUP_TOP", 4)
    ],
    # Unary ops 
    "UNARY_POSITIVE": [
        ("UNARY_POSITIVE", 5)
    ],
    "UNARY_NEGATIVE": [
        ("UNARY_NEGATIVE", 6)
    ],
    "UNARY_NOT": [
        ("UNARY_NOT", 7)
    ],
    "UNARY_INVERT": [
        ("UNARY_INVERT", 8)
    ],
    "GET_ITER": [
        ("GET_ITER", 9)
    ],
    "GET_YIELD_FROM_ITER": [
        ("GET_YIELD_FROM_ITER", 10)
    ],
    # Binary ops
    "BINARY_POWER": [
        ("BINARY_POWER", 11)
    ],
    "BINARY_MULTIPLY": [
        ("BINARY_MULTIPLY", 12)
    ],
    "BINARY_MATRIX_MULTIPLY": [
        ("BINARY_MATRIX_MULTIPLY", 13)
    ],
    "BINARY_FLOOR_DIVIDE": [
        ("BINARY_FLOOR_DIVIDE", 14)
    ],
    "BINARY_TRUE_DIVIDE": [
        ("BINARY_TRUE_DIVIDE", 15)
    ],
    "BINARY_MODULO": [
        ("BINARY_MODULO", 16)
    ],
    "BINARY_ADD": [
        ("BINARY_ADD", 17)
    ],
    "BINARY_SUBTRACT": [
        ("BINARY_SUBTRACT", 18)
    ],
    "BINARY_SUBSCR": [
        ("BINARY_SUBSCR", 19)
    ],
    "BINARY_LSHIFT": [
        ("BINARY_LSHIFT", 20)
    ],
    "BINARY_RSHIFT": [
        ("BINARY_RSHIFT", 21)
    ],
    "BINARY_AND": [
        ("BINARY_AND", 22)
    ],
    "BINARY_XOR": [
        ("BINARY_XOR", 23)
    ],
    "BINARY_OR": [
        ("BINARY_OR", 24)
    ],
    # In-place operations
    "INPLACE_POWER": [
        ("INPLACE_POWER", 25)
    ],
    "INPLACE_MULTIPLY": [
        ("INPLACE_MULTIPLY", 26)
    ],
    "INPLACE_MATRIX_MULTIPLY": [
        ("INPLACE_MATRIX_MULTIPLY", 27)
    ],
    "INPLACE_FLOOR_DIVIDE": [
        ("INPLACE_FLOOR_DIVIDE", 28)
    ],
    "INPLACE_TRUE_DIVIDE": [
        ("INPLACE_TRUE_DIVIDE", 29)
    ],
    "INPLACE_MODULO": [
        ("INPLACE_MODULO", 30)
    ],
    "INPLACE_ADD": [
        ("INPLACE_ADD", 31)
    ],
    "INPLACE_SUBTRACT": [
        ("INPLACE_SUBTRACT", 32)
    ],
    "INPLACE_LSHIFT": [
        ("INPLACE_LSHIFT", 33)
    ],
    "INPLACE_RSHIFT": [
        ("INPLACE_RSHIFT", 34)
    ],
    "INPLACE_AND": [
        ("INPLACE_AND", 35)
    ],
    "INPLACE_XOR": [
        ("INPLACE_XOR", 36)
    ],
    "INPLACE_OR": [
        ("INPLACE_OR", 37)
    ],
    # Subscription operations
    "STORE_SUBSCR": [
        ("STORE_SUBSCR", 38)
    ],
    "DELETE_SUBSCR": [
        ("DELETE_SUBSCR", 39)
    ],
    # Coroutine operations
    "GET_AWAITABLE": [
        ("GET_AWAITABLE", 40)
    ],
    "GET_AITER": [
        ("GET_AITER", 41)
    ],
    "GET_ANEXT": [
        ("GET_ANEXT", 42)
    ],
    "END_ASYNC_FOR": [
        ("END_ASYNC_FOR", 43)
    ],
    "BEFORE_ASYNC_WITH": [
        ("BEFORE_ASYNC_WITH", 44)
    ],
    "SETUP_ASYNC_WITH": [
        ("SETUP_ASYNC_WITH", 45)
    ],

    # Miscellaneous operations
    "PRINT_EXPR": [
        ("PRINT_EXPR", 46)
    ],
    "SET_ADD": [
        ("SET_ADD", 47)
    ],
    "LIST_APPEND": [
        ("LIST_APPEND", 48)
    ],
    "MAP_ADD": [
        ("MAP_ADD", 49)
    ],
    "RETURN_VALUE": [
        ("RETURN_VALUE", 50)
    ],
    "YIELD_VALUE": [
        ("YIELD_VALUE", 51)
    ],
    "YIELD_FROM": [
        ("YIELD_FROM", 52)
    ],
    "SETUP_ANNOTATIONS": [
        ("SETUP_ANNOTATIONS", 53)
    ],
    "IMPORT_STAR": [
        ("IMPORT_STAR", 54)
    ],
    "POP_BLOCK": [
        ("POP_BLOCK", 55)
    ],
    "POP_EXCEPT": [
        ("POP_EXCEPT", 56)
    ],
    "RERAISE": [
        ("RERAISE", 57)
    ],
    "WITH_EXCEPT_START": [
        ("WITH_EXCEPT_START", 58)
    ],
    "LOAD_ASSERTION_ERROR": [
        ("LOAD_ASSERTION_ERROR", 59)
    ],
    "LOAD_BUILD_CLASS": [
        ("LOAD_BUILD_CLASS", 60)
    ],
    "SETUP_WITH": [
        ("SETUP_WITH", 61)
    ],

    # Opcodes using their arguments
    "STORE_NAME": [
        ("STORE_NAME", 62)
    ],
    "DELETE_NAME": [
        ("DELETE_NAME", 63)
    ],
    "UNPACK_SEQUENCE": [
        ("UNPACK_SEQUENCE", 64)
    ],
    "UNPACK_EX": [
        ("UNPACK_EX", 65)
    ],
    "STORE_ATTR": [
        ("STORE_ATTR", 66)
    ],
    "DELETE_ATTR": [
        ("DELETE_ATTR", 67)
    ],
    "STORE_GLOBAL": [
        ("STORE_GLOBAL", 68)
    ],
    "DELETE_GLOBAL": [
        ("DELETE_GLOBAL", 69)
    ],
    "LOAD_CONST": [
        ("LOAD_CONST", 70)
    ],
    "LOAD_NAME": [
        ("LOAD_NAME", 71)
    ],
    "BUILD_TUPLE": [
        ("BUILD_TUPLE", 72)
    ],
    "BUILD_LIST": [
        ("BUILD_LIST", 73)
    ],
    "BUILD_SET": [
        ("BUILD_SET", 74)
    ],
    "BUILD_MAP": [
        ("BUILD_MAP", 75)
    ],
    "BUILD_CONST_KEY_MAP": [
        ("BUILD_CONST_KEY_MAP", 76)
    ],
    "BUILD_STRING": [
        ("BUILD_STRING", 77)
    ],
    "LIST_TO_TUPLE": [
        ("LIST_TO_TUPLE", 78)
    ],
    "LIST_EXTEND": [
        ("LIST_EXTEND", 79)
    ],
    "SET_UPDATE": [
        ("SET_UPDATE", 80)
    ],
    "DICT_UPDATE": [
        ("DICT_UPDATE", 81)
    ],
    "DICT_MERGE": [
        ("DICT_MERGE", 82)
    ],
    "LOAD_ATTR": [
        ("LOAD_ATTR", 83)
    ],
    "COMPARE_OP": [
        ("COMPARE_OP", 84)
    ],
    "IS_OP": [
        ("IS_OP", 85)
    ],
    "CONTAINS_OP": [
        ("CONTAINS_OP", 86)
    ],
    "IMPORT_NAME": [
        ("IMPORT_NAME", 87)
    ],
    "IMPORT_FROM": [
        ("IMPORT_FROM", 88)
    ],
    "JUMP_FORWARD": [
        ("JUMP_FORWARD", 89)
    ],
    "POP_JUMP_IF_TRUE": [
        ("POP_JUMP_IF_TRUE", 90)
    ],
    "POP_JUMP_IF_FALSE": [
        ("POP_JUMP_IF_FALSE", 91)
    ],
    "JUMP_IF_NOT_EXC_MATCH": [
        ("JUMP_IF_NOT_EXC_MATCH", 92)
    ],
    "JUMP_IF_TRUE_OR_POP": [
        ("JUMP_IF_TRUE_OR_POP", 93)
    ],
    "JUMP_IF_FALSE_OR_POP": [
        ("JUMP_IF_FALSE_OR_POP", 94)
    ],
    "JUMP_ABSOLUTE": [
        ("JUMP_ABSOLUTE", 95)
    ],
    "FOR_ITER": [
        ("FOR_ITER", 96)
    ],
    "LOAD_GLOBAL": [
        ("LOAD_GLOBAL", 97)
    ],
    "SETUP_FINALLY": [
        ("SETUP_FINALLY", 98)
    ],
    "LOAD_FAST": [
        ("LOAD_FAST", 99)
    ],
    "STORE_FAST": [
        ("STORE_FAST", 100)
    ],
    "DELETE_FAST": [
        ("DELETE_FAST", 101)
    ],
    "LOAD_CLOSURE": [
        ("LOAD_CLOSURE", 102)
    ],
    "LOAD_DEREF": [
        ("LOAD_DEREF", 103)
    ],
    "LOAD_CLASSDEREF": [
        ("LOAD_CLASSDEREF", 104)
    ],
    "STORE_DEREF": [
        ("STORE_DEREF", 105)
    ],
    "DELETE_DEREF": [
        ("DELETE_DEREF", 106)
    ],
    "RAISE_VARARGS": [
        ("RAISE_VARARGS", 107)
    ],
    "CALL_FUNCTION": [
        ("CALL_FUNCTION", 108)
    ],
    "CALL_FUNCTION_KW": [
        ("CALL_FUNCTION_EX", 109)
    ],
    "CALL_FUNCTION_EX": [
        ("CALL_FUNCTION_EX", 110)
    ],
    "LOAD_METHOD": [
        ("LOAD_METHOD", 111)
    ],
    "CALL_METHOD": [
        ("CALL_METHOD", 112)
    ],
    "MAKE_FUNCTION": [
        ("MAKE_FUNCTION", 113)
    ],
    "BUILD_SLICE": [
        ("BUILD_SLICE", 114)
    ],
    "EXTENDED_ARG": [
        ("EXTENDED_ARG", 115)
    ],
    "FORMAT_VALUE": [
        ("FORMAT_VALUE", 116)
    ],
    "HAVE_ARGUMENT": [
        ("HAVE_ARGUMENT", 117)
    ]
}