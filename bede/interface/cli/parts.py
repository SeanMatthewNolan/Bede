import console
from console.utils import wait_key
from console.constants import ESC
import prompt_toolkit

EXIT_KEYS = (ESC, 'q')

# http://microvga.com/ansi-keycodes
EXTENDED_KEY_CODES = {
    chr(15): 'tab',
    chr(59): 'f1',
    chr(60): 'f2',
    chr(61): 'f3',
    chr(62): 'f4',
    chr(63): 'f5',
    chr(64): 'f6',
    chr(65): 'f7',
    chr(66): 'f8',
    chr(67): 'f9',
    chr(68): 'f10',
    chr(133): 'f11',
    chr(134): 'f12',
    chr(71): 'home',
    chr(72): 'up_arrow',
    chr(73): 'page_up',
    chr(75): 'left_arrow',
    chr(77): 'right_arrow',
    chr(79): 'end',
    chr(80): 'down_arrow',
    chr(81): 'page_down',
    chr(82): 'insert',
    chr(83): 'delete',
    chr(3): 'null',
}


def wait_extended_key():
    key = wait_key()
    if key == chr(0):
        key = EXTENDED_KEY_CODES[wait_key()]

    return key


def cursor_test():
    for idx in range(10):
        print(f'{idx}---------')

    key = ''
    while key not in EXIT_KEYS:
        key = wait_extended_key()
        print(key)


