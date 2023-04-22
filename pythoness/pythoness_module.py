import inspect
import io
import json
import re
import sys
import textwrap
import openai
import sqlite3

import ast_comments as ast

from functools import wraps
from typing import Callable, Tuple


def is_type_compatible(f: Callable, g: Callable) -> bool:
    f_sig = inspect.signature(f)
    g_sig = inspect.signature(g)

    # Check number of parameters
    if len(f_sig.parameters) != len(g_sig.parameters):
        return False

    # Check parameter types
    for f_param, g_param in zip(f_sig.parameters.values(), g_sig.parameters.values()):
        f_type = f_param.annotation
        g_type = g_param.annotation

        # If the second function's type is missing or Any, and the first function's type is not, they are compatible.
        if g_type is inspect.Parameter.empty or g_type is type(None):
            continue
        elif f_type is inspect.Parameter.empty or f_type is type(None):
            # For now, we consider this to be compatible.
            continue
            #if not issubclass(type(None), g_type):
            #    return False

        if not issubclass(g_type, f_type) and not issubclass(f_type, g_type):
            return False

    # Check return type
    f_return_type = f_sig.return_annotation
    g_return_type = g_sig.return_annotation

    # If the second function's return type is missing or Any, and the first function's return type is not, they are compatible.
    if g_return_type is inspect.Parameter.empty or g_return_type is type(None):
        return True
    elif f_return_type is inspect.Parameter.empty or f_return_type is type(None):
        if issubclass(type(None), g_return_type):
            return True
        else:
            return False

    if not issubclass(g_return_type, f_return_type) and not issubclass(f_return_type, g_return_type):
        return False

    return True


class CodeDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompt_code (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                code TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
        CREATE INDEX IF NOT EXISTS index_prompt ON prompt_code (prompt)
        """)
        self.connection.commit()
    
    def insert_code(self, prompt, code):
        self.cursor.execute("INSERT INTO prompt_code (prompt, code) VALUES (?, ?)", (prompt, code))
        self.connection.commit()
    
    def get_code(self, prompt):
        self.cursor.execute("SELECT code FROM prompt_code WHERE prompt = ?", (prompt,))
        row = self.cursor.fetchone()
        if row is not None:
            return row[0]
        else:
            return None
    
    def close(self):
        self.connection.close()


def complete(user_prompt):
    try:
        completion = openai.ChatCompletion.create(
            # For now, hard code
            model="gpt-4", # args["llm"],
            request_timeout=30, # args["timeout"],
            messages=[{"role": "user", "content": user_prompt}],
        )
        return completion.choices[0].message.content
    except openai.error.AuthenticationError:
        print("You need an OpenAI key to use this tool.")
        print("You can get a key here: https://platform.openai.com/account/api-keys")
        print("Set the environment variable OPENAI_API_KEY to your key value.")
        print(
            "If OPENAI_API_KEY is already correctly set, you may have exceeded your usage or rate limit."
        )
    except openai.error.Timeout:
        print(
            "The OpenAI API timed out. You can try increasing the timeout with the --timeout option."
        )
    sys.exit(1)
    

def spec(string, replace=False, tests=None, max_retries=3):
    def decorator(func):
        cached_function = None
        cdb = CodeDatabase("pythoness-cache.db")
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal cdb, cached_function
            # If we've already built this function and cached it,
            # just run it.
            if cached_function:
                return cached_function(*args, **kwargs)
            # We need to generate a function from the spec.
            # We populate the prompt with the function's name, argument name and types, and the return type.
            function_name = func.__name__
            arg_types = []
            for arg_name, arg_value in zip(func.__code__.co_varnames, args):
                arg_types.append((arg_name, type(arg_value)))
            for kwarg_name, kwarg_value in kwargs.items():
                arg_types.append((kwarg_name, type(kwarg_value),))
            return_type = func.__annotations__.get('return', None)
                
            prompt = f"""

            Produce a JSON object with code for a Python function named {function_name}
            that performs the following task as a filed \"code\".
            Only produce output that can be parsed as JSON.
            
            Task: {string}

            Include a docstring containing the task description above.
            """

            if tests:
                test_string = "            \n".join(tests)
                prompt += f"""
            The function should pass the following tests:

            {test_string}
                """
                
            prompt += f"""
            The function should have the following argument types and return type:
            
            Arguments: {arg_types}
            Return type: {return_type}
            """
            # See if we already have code corresponding to that prompt in the database.
            function_def = cdb.get_code(prompt)
            retries = 0
            failing_tests = set()
            while retries < max_retries:
                retries += 1
                # Retry until success.
                if not function_def:
                    result = complete(prompt)
                    try:
                        the_json = json.loads(result)
                    except:
                        # JSON parse failure: retry.
                        continue
                    function_def = the_json["code"]
                # Try to compile the function
                try:
                    compiled = compile(function_def, "<string>", "exec")
                except:
                    # Compilation failed: retry.
                    continue
                # If we get here, we can run the function and use it going forwards.
                exec(compiled, globals())
               
                fn = globals()[function_name]
                if not is_type_compatible(func, fn):
                    # Function types don't validate. Retry.
                    continue
                
                # Validate tests.
                if tests:
                    for t in tests:
                        if not eval(t):
                            failing_tests.add(t)
                if len(failing_tests) > 0:
                    # At least one test failed. Retry.
                    continue

                # Validated. Cache the function and persist it.
                cached_function = fn
                cdb.insert_code(prompt, function_def)
                # If selected, replace the function definition
                # in the file.
                if replace:
                    import inspect
                    frame = inspect.currentframe()
                    frame = frame.f_back
                    file_name = frame.f_code.co_filename
                    with open(file_name, "r") as file:
                        source = file.read()
                    tree = ast.parse(source)
                    # Find the function with the given name and replace it with the new function.
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
                            node_index = tree.body.index(node)
                            fn_body = ast.parse(function_def).body
                            tree.body[node_index] = fn_body
                            
                    new_source = ast.unparse(tree)

                    # Update the file.
                    with open(file_name, "w") as f:
                        f.write(new_source)
                
                return cached_function(*args, **kwargs)
            # If we got here, we had too many retries.
            if failing_tests:
                raise Exception(f"Maximum number of retries exceeded ({max_retries}).\nFailing tests: {failing_tests}")
            else:
                raise Exception(f"Maximum number of retries exceeded ({max_retries}).")
                
        return wrapper
    return decorator

