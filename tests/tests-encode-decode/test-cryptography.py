import pythoness

def encode(input_string):
    encoded_string = ""
    
    for char in input_string:
        if char.isalpha():  # Check if the character is a letter
            if char.islower():  # Check if the character is a lowercase letter
                # Shift the character and wrap around using modulo
                encoded_char = chr((ord(char) - ord('a') + 1) % 26 + ord('a'))
            elif char.isupper():  # Check if the character is an uppercase letter
                # Shift the character and wrap around using modulo
                encoded_char = chr((ord(char) - ord('A') + 1) % 26 + ord('A'))
        else:
            encoded_char = char  # Keep non-alphabet characters unchanged
        
        encoded_string += encoded_char
    
    return encoded_string


@pythoness.spec("""Decode str into the string inputted into an encode() function. 
                Here is a sample input and output to the encode() function:
                encode('zAp') == 'aBq'""", tests=[({'s':"text(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')"}, "decode(encode(s)) == s")])

def decode(str : str):
    ""

assert(decode(encode("apple")) == "apple")
