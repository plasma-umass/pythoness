# Pythoness

Pythoness is a Python module that uses OpenAI's GPT-4 model to automatically generate Python code based on natural language descriptions of the desired functionality.

## Installation

The easiest way to install Pythoness is through pip:

```bash
python3 -m pip install pythoness
```

## Usage

To use Pythoness, you will need to import the `pythoness` module and use the `@pythoness.spec` decorator to specify the desired functionality. Here is an example usage:

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

Pythoness caches the results of translating natural language to Python, so subsequent executions in the same directory will run much faster.

