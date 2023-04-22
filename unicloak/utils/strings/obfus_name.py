import random 


def obfus_name(keys=["I", "ḻ", "l", "ἰ"], n=12):
    """
    Obfuscates a name by generating a random string from keys of length n

    Args:
        keys (list): List of chars to be used in obfuscation
        n (int): Length of generated name

    Returns:
        str: The obfuscated string
    """
    return ''.join([random.choice(keys) for _ in range(n)])