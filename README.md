# Pythoness

> Pythoness: The priestess of the oracle of Apollo at Delphi.

by [Emery Berger](https://emeryberger.com)

[![PyPI Latest Release](https://img.shields.io/pypi/v/pythoness.svg)](https://pypi.org/project/pythoness/)[![Downloads](https://pepy.tech/badge/pythoness)](https://pepy.tech/project/pythoness) [![Downloads](https://pepy.tech/badge/pythoness/month)](https://pepy.tech/project/pythoness) ![Python versions](https://img.shields.io/pypi/pyversions/pythoness.svg?style=flat-square)

Pythoness is a Python module that automatically generates Python code based on natural language descriptions of the desired functionality.

*NOTE*: To use pythoness, you must first set up an OpenAI API key. If you
already have an API key, you can set it as an environment variable
called `OPENAI_API_KEY`. If you do not have one yet,
you can get a key here: https://platform.openai.com/account/api-keys

```
export OPENAI_API_KEY=<your-api-key>
```

## Installation

The easiest way to install Pythoness is through pip:

```bash
python3 -m pip install pythoness
```

## Usage

To use Pythoness, you just import the `pythoness` module and then use the `@pythoness.spec` decorator to specify the desired functionality. Here is an:

```python
import pythoness

@pythoness.spec("Compute the nth number in the Fibonacci series.")
def myfib(n: int) -> int:
    ""
```

This code will generate a Python function named `myfib` that computes the nth number in the Fibonacci series.

To actually execute the function, you can call it as you would any other Python function:

```python
for i in range(20):
    print(myfib(i))
```

Pythoness caches the results of translating natural language to
Python, so subsequent executions in the same directory will run much
faster.

If you want Pythoness to replace the code with the generated function, just add `replace=True`:

```python
@pythoness.spec("Compute the nth number in the Fibonacci series.", replace=True)
def myfib(n: int) -> int:
    ""
```

Setting the `replace` flag will cause Pythoness to rewrite the program with the synthesized function definition(s).

