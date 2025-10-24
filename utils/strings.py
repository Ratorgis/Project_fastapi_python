import re
import random
import string

_letters = string.digits + string.ascii_letters

def rand_string(k: int) -> str:
    return ''.join(random.choices(_letters, k = k))

def auto_complete_link(link: str) -> str:
    link_test = link.split('://')
    if link_test[0] not in ['https', 'http']:
        return 'https://' + link[-1]
    return link

def link_valid(link: str) -> bool:
    reg = r"(\w+://\w+.\w+)"
    if len(re.findall(reg, link)[0]) != len(link):
        return False
    return True

