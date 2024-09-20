import pythoness

class Encode:
    def encode(input_string):
        """ turns a string into a list of tuples containing each
        letter in the input string and how many times it appears, in the order
        they appear in."""
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

class Wrap:
    def apple():
        ""


    class Decode:
        @pythoness.spec("""Decode lst into the string inputted into an encode() function.""", 
                    tests=["Wrap.Decode.decode(Encode.encode('s')) == 's'"], related_objs=[Encode.encode], verbose = True)
        def decode(lst : list) -> str:
            ""

print(Wrap.Decode.decode(Encode.encode("apple")))