import pythoness

def encode(s):
    """
    A simple single Caesar shift
    """
    shift = 1
    result = []
    for char in s:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            result.append(chr(start + (ord(char) - start + shift) % 26))
        else:
            result.append(char)
    return ''.join(result)
assert encode('abcdefghijklmnopqrstuvwxyz') == 'bcdefghijklmnopqrstuvwxyza'
assert encode('abcdefghijklmnopqrstuvwxyz'.upper()) == 'bcdefghijklmnopqrstuvwxyza'.upper()