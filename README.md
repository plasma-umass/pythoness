# Snakelang

Snakelang is a Python module that uses OpenAI's GPT-4 model to automatically generate Python code based on natural language descriptions of the desired functionality.

## Installation

The easiest way to install Snakelang is through pip:

```bash
python3 -m pip install snakelang
```

## Usage

To use Snakelang, you will need to import the `snakelang` module and use the `@snakelang.spec` decorator to specify the desired functionality. Here is an example usage:

```python
import snakelang

@snakelang.spec("Compute the nth number in the Fibonacci series.")
def myfib(n: int) -> int:
    ""
```

This code will generate a Python function named `myfib` that computes the nth number in the Fibonacci series.

To actually execute the function, you can call it as you would any other Python function:

```python
for i in range(20):
    print(myfib(i))
```

Snakelang caches the results of translating natural language to Python, so subsequent executions in the same directory will run much faster.

