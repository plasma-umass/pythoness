import pythoness

@pythoness.spec("""Given a positive, non-zero decimal number num, return 1 if num
                when converted to a binary number contains an odd number of 0's,
                and 0 otherwise""",
                tests=["bit_parity(245)==0", "bit_parity(113)==1",
                       "bit_parity(112)==0", "bit_parity(145)==1"], model="gpt-4", verbose=True)


def bit_parity(num : int) -> int:
    ""

print("Running tests: bit-parity")
# assert(bit_parity(145) == 1)
assert(bit_parity(1) == 0)
assert(bit_parity(547) == 0)
assert(bit_parity(330) == 1)
print("Tests complete.")