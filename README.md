# Pythoness

![Pythoness](https://raw.githubusercontent.com/plasma-umass/pythoness/main/pythoness-logo.jpg)

_Pythoness: The priestess of the oracle of Apollo at Delphi._

Pythoness by [Emery Berger](https://emeryberger.com), extension by Kyle Gwilt and Stephen Freund

[![PyPI Latest Release](https://img.shields.io/pypi/v/pythoness.svg)](https://pypi.org/project/pythoness/)[![Downloads](https://static.pepy.tech/badge/pythoness)](https://pepy.tech/project/pythoness) [![Downloads](https://static.pepy.tech/badge/pythoness/month)](https://pepy.tech/project/pythoness) ![Python versions](https://img.shields.io/pypi/pyversions/pythoness.svg?style=flat-square)

Pythoness automatically generates Python code from natural language descriptions and tests.

> **Note**
> Pythoness needs to be connected to an LLM in order to function. Below is an example for how to connect Pythoness with an OpenAI account. For other LLMs, consult their documentation.
>
> [OpenAI account](https://openai.com/api/). _Your account will need to have a positive balance for this to work_ ([check your balance](https://platform.openai.com/account/usage)). If you have never purchased credits, you will need to purchase at least $1 in credits (if your API account was created before August 13, 2023) or $0.50 (if you have a newer API account). [Get a key here.](https://platform.openai.com/account/api-keys)
>
> Once you have an API key, set it as an environment variable called `OPENAI_API_KEY`.
>
> ```bash
> export OPENAI_API_KEY=<your-api-key>
> ```

## Installation

The easiest way to install Pythoness is through pip: 

```bash
python3 -m pip install pythoness
```

## Usage

To use Pythoness, you just import the `pythoness` module and then use the `@pythoness.spec` decorator to specify the desired functionality:

```python
import pythoness

@pythoness.spec("Compute the nth number in the Fibonacci series.")
def myfib(n: int) -> int:
    ""
```

This code will internally generate a Python function named `myfib`
that computes the nth number in the Fibonacci series.  To actually
execute the function, you can call it as you would any other Python
function:

```python
for i in range(20):
    print(myfib(i))
```

Pythoness caches the results of translating natural language to
Python, so subsequent executions in the same directory will run much
faster (Pythoness creates a database called `pythoness-cache.db` that
saves these translations).

To turn off all logging messages, use the `PYNS_QUIET` environment variable:

```bash
env PYNS_QUIET=1 python3 myfib.py 
```


### Incorporating tests

You can guide Pythoness by providing some tests. Pythoness will use
tests both to generate the Python code and to validate it. Tests are just
a list of strings containing Python code or functions which should all evaluate to `True`.

```python
@pythoness.spec("Compute the nth number in the Fibonacci series.",
                tests=["myfib(1) == 1", "myfib(2) == 1"])
def myfib(n: int) -> int:
    ""
```

You can also guide Pythoness with _property-based tests_. To do this,
describe the properties that you want your program to
exhibit. Pythoness will run a property-based tester
([Hypothesis](https://github.com/HypothesisWorks/hypothesis/tree/master/hypothesis-python)),
which will perform tests many times to ensure that the generated
function meets the specified properties. This approach is much more
powerful than the unit tests described above.

```python
@pythoness.spec("Compute the nth number in the Fibonacci series.",tests = [({'n':'integers(1,20)'}, "myfib(n+2) == myfib(n+1)+myfib(n)")])
def myfib(n: int) -> int:
    ""
```

TestCases from the built in [unittest](https://docs.python.org/3/library/unittest.html) framework are the final option for testing, and can be used by giving Pythoness TestCases or a module of TestCases:

```python
@pythoness.spec("Compute the nth number in the Fibonacci series.", tests = [testmodule.TestFib])
def myfib(n: int) -> int:
    ""
```

### Incorporating other objects

You can further guide Pythoness by giving it functions and classes that are related
to the code that it will be generating. It uses the docstring of provided functions 
and classes to understand their purpose. Pythoness can make use of functions that will be generated 
by itself this way, where the docstring is specified in `spec`.
 
`related_objs` is a list that can include functions, classes, or special strings:
* `'cls'` which represents everything in the class the generated function is contained in,
besides itself
* `'*'` which represents everything in the file the generated function is contained in,
besides itself

```python
@pythoness.spec("Encodes a string using a single-shift Caesar cipher")
def encode(s : str) -> str:
    ""

@pythoness.spec("Decodes a string given to encode()", related_objs = [encode])
def decode(s : str) -> str:
    ""
```

When working with classes, it's best to use Python's `__slots__` feature. While Pythoness can function without it, this increases Pythoness' consistency.

### Replacing Pythoness functions with Python

You can have Pythoness to replace the spec directly in your file with
the generated function: just add `replace=True':

```python
@pythoness.spec("Compute the nth number in the Fibonacci series.",
                tests=["myfib(1) == 1", "myfib(2) == 1"],
		replace=True)
def myfib(n: int) -> int:
    ""
```

For example, Pythoness produced this code:

```
def myfib(n: int) -> int:
    """
    Compute the nth number in the Fibonacci series.

    :param n: The position of the desired number in the Fibonacci series
    :type n: int
    :return: The nth number in the Fibonacci series
    :rtype: int
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    elif n == 1 or n == 2:
        return 1
    else:
        fib1, fib2 = 1, 1
        for _ in range(3, n + 1):
            fib1, fib2 = fib2, fib1 + fib2
        return fib2
```

You can also replace every generated function using the 'PYNS_REPLACE' environment variable:
```bash
env 'PYNS_REPLACE'=1
```

### Other ways to control Pythoness

Pythoness offers a few other ways to control its behavior. These are
all arguments to `spec`. The provided values indicate the the default
value.

* `max_retries=3`: controls the maximum number of retries due to failures (e.g., a function that fails one of the provided tests).

* `model='gpt-4o'`: controls which LLM model to query

* `timeout_seconds=0`: sets the amount of time for a single Pythoness attempt to timeout. By default, there is no timeout.

* `verbose=False`: set this to `True` to have Pythoness to output details as it generates and validates code. Mostly useful for developers and for keeping tabs on progress. Can be set
for every function at once using the 'PYNS_VERBOSE' environment variable.

* `regenerate=False`: set this to `True` to generate new code every time a function is called, rather than store it and reuse it. 

* `output=False`: set this to `True` to have Pythoness output the generated code the first time the function is called.



