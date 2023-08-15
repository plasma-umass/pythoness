import pythoness

@pythoness.spec("Compute the nth number in the Fibonacci series.",tests = [({'n':'integers(1,20)'}, "myfib(n+2) == myfib(n+1)+myfib(n)")])
def myfib(n: int) -> int:
    ""

for i in range(20):
    print(myfib(i))
