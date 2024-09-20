import pythoness
import string

# Define the plaintext and cipher alphabets
plaintext_alphabet = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
cipher_alphabet = 'zyxwvutsrqponmlkjihgfedcba'  # Example cipher alphabet

def encode(plaintext, plaintext_alphabet=plaintext_alphabet, cipher_alphabet=cipher_alphabet):
    # Create a mapping of plaintext characters to cipher characters
    substitution_map = {p: c for p, c in zip(plaintext_alphabet, cipher_alphabet)}
    
    # Encode the plaintext by substituting each character
    ciphertext = ''.join(substitution_map.get(char, char) for char in plaintext)
    
    return ciphertext

print(encode('wpamtbwikx'))

@pythoness.spec("""Decode str into the string inputted into an encode() function. 
                The encode function maps each character in the string to the corresponding
                letter on the opposite end of the alphabet.""", tests=[({'s':"text(alphabet='abcdefghijklmnopqrstuvwxyz')"}, "decode(encode(s)) == s")])

def decode(str : str) -> str:
    ""

assert(decode(encode("apple")) == 'apple')