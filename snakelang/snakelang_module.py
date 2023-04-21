import io
import json
import re
import sys
import textwrap
import openai
import sqlite3

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
    

def spec(string):
    def decorator(func):
        cached_function = None
        cdb = CodeDatabase("snake.db")
        def wrapper(*args, **kwargs):
            nonlocal cdb, cached_function
            if cached_function:
                return cached_function(*args, **kwargs)
            # Build prompt
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
            
            {string}

            The function should have the following argument types and return type:
            
            Arguments: {arg_types}
            Return type: {return_type}
            """
            # print(prompt)
            # See if we already have code for that prompt.
            function_def = cdb.get_code(prompt)
            if not function_def:
                result = complete(prompt)
                # print(result)
                #try:
                the_json = json.loads(result)
                function_def = the_json["code"]
            else:
                pass
            compiled = compile(function_def, "<string>", "exec") # ast.unparse(get_function_body(function_def))
            exec(compiled, globals())
            cached_function = globals()[function_name]
            cdb.insert_code(prompt, function_def)
            return cached_function(*args, **kwargs)
        return wrapper
    return decorator

