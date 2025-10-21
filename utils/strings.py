import random
import string

_letters = string.digits + string.ascii_letters

def rand_string(k: int) -> str:
    return ''.join(random.choices(_letters, k = k))
