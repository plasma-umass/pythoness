import pythoness

def encode(input_string):
    count = 1
    prev = ""
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                entry = (prev, count)
                lst.append(entry)
            count = 1
            prev = character
        else:
            count += 1
    entry = (character, count)
    lst.append(entry)
    return lst

@pythoness.spec("Decode lst into the string inputted into the above encode function", tests=[("decode(encode('s')) == 's'")])

def decode(lst : list) -> str:
    ""

print(decode(encode("apple")))