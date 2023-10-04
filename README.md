# Pythoness

![Pythoness](https://raw.githubusercontent.com/plasma-umass/pythoness/main/pythoness-logo.jpg)

_Pythoness: The priestess of the oracle of Apollo at Delphi._

by [Emery Berger](https://emeryberger.com)

[![PyPI Latest Release](https://img.shields.io/pypi/v/pythoness.svg)](https://pypi.org/project/pythoness/)[![Downloads](https://static.pepy.tech/badge/pythoness)](https://pepy.tech/project/pythoness) [![Downloads](https://static.pepy.tech/badge/pythoness/month)](https://pepy.tech/project/pythoness) ![Python versions](https://img.shields.io/pypi/pyversions/pythoness.svg?style=flat-square)

Pythoness automatically generates Python code from natural language descriptions and tests.

> **Note**
>
> Pythoness needs to be connected to an [OpenAI account](https://openai.com/api/). _Your account will need to have a positive balance for this to work_ ([check your balance](https://platform.openai.com/account/usage)). If you have never purchased credits, you will need to purchase at least $1 in credits (if your API account was created before August 13, 2023) or $0.50 (if you have a newer API account) in order to have access to GPT-4, which Pythoness uses. [Get a key here.](https://platform.openai.com/account/api-keys)
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

### Incorporating tests

You can guide Pythoness by providing some tests. Pythoness will use
tests both to generate the Python code and to validate it. Tests are just
a list of strings containing Python code which should all evaluate to `True`.

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


### Replacing Pythoness functions with Python

You can have Pythoness to replace the spec directly in your file with
the generated function: just add `replace=True`:

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

### Other ways to control Pythoness

Pythoness offers a few other ways to control its behavior. These are
all arguments to `spec`. The provided values indicate the the default
value.

* `max_retries=3`: controls the maximum number of retries due to failures (e.g., a function that fails one of the provided tests).

* `min_confidence=0.7`: sets the minimum level of confidence that the AI system reports regarding the correctness of the generated function (a number between 0 and 1, corresponding to 0% and 100%). Increasing the confidence level may require increasing `max_retries`.

* `verbose=False`: set this to `True` to have Pythoness to output details as it generates and validates code. Mostly useful for developers and for keeping tabs on progress.

* `output=False`: set this to `True` to have Pythoness output the generated code the first time the function is called.

