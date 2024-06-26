from . import assistant
from . import logger
from . import exceptions
from . import timeout
import textwrap
import json
import ast_comments as ast


debug_print = False


def get_function_info(func, *args, **kwargs):
    ret = {}
    ret['function_name'] = func.__name__
    ret['arg_types'] = []
    for arg_name, arg_value in zip(func.__code__.co_varnames, args):
        ret['arg_types'].append((arg_name, type(arg_value)))  # FIXME: use annotations if available
    for kwarg_name, kwarg_value in kwargs.items():
        ret['arg_types'].append((kwarg_name, type(kwarg_value)))  # FIXME: use annotations if available
    ret['return_type'] = func.__annotations__.get('return', None)
    return ret

def prep_tests(tests):
    ''' Takes a string of tests as input and prepares a string that will be appended to the prompt '''
    final_tests = []
    for t in tests:
        if isinstance(t, tuple):
            final_tests.append(t[1])
        elif isinstance(t, str):
            final_tests.append(t)
        else:
            pass
    test_string = '\n'.join(final_tests)
    prompt_string = f'\n        The function should pass the following tests:\n        {test_string}\n    '
    return prompt_string

def create_prompt(function_info, string, tests):
    prompt = f"""
        Produce a JSON object with code for a Python function
        named {function_info['function_name']} that performs the following task as
        a field \"code\". Only produce output that can be parsed as
        JSON.  

        Task:
        {textwrap.dedent(string)}

        Include a docstring containing the task description above
        (without the word "Task:").  The function should be
        entirely self-contained, with all imports, code, and data
        required for its functionality. Do not include any tests in
        the function. """
    
    if tests:
        prompt += prep_tests(tests)

    prompt += f"""
        The function should have the following argument types and return type:

        Arguments: {function_info['arg_types']}
        Return type: {function_info['return_type']}
        """

    return prompt

def replace_func(frame, function_name, function_def):
    frame = frame.f_back
    file_name = frame.f_code.co_filename
    with open(file_name, 'r') as file:
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
    with open(file_name, 'w') as f:
        f.write(new_source)

def database_compile(function_info, function_def, *args, **kwargs):
    ''' Compiles and executes a function with information from the CodeDatabase '''
    compiled = compile(function_def, '<string>', 'exec')
    exec(compiled, globals())
    fn = globals()[function_info['function_name']]
    return fn(*args, **kwargs)

def setup_info(function_info, func, string, prompt):
    ''' Creates the function_info dictionary '''
    function_info.update({
        "spec" : string,
        "retries" : 0,
        "function_def" : None,
        "compiled" : None,
        "globals" : func.__globals__,
        "original_prompt" : prompt
    })
    return function_info 

def parse_func(function_info, client: assistant.Assistant, prompt, verbose, log : logger.Logger):
    ''' Using Assistant, queries the LLM and places returned information in function_info '''
    result = client.query(prompt)
    function_info['completion'] = result

    try:
        the_json = json.loads(result)
    except:
        # JSON parse failure: retry
        raise exceptions.JSONException()
    
    function_def = the_json['code']

    if verbose:
        log.log('[Pythoness] Synthesized function: \n', function_def)

    function_info['function_def'] = function_def
    
    return function_info

def compile_func(function_info):
    ''' Compiles the function_def stored in info '''
    try:
        compiled = compile(function_info['function_def'], '<string>', 'exec')
        function_info['compiled'] = compiled
        return function_info
    except:
        # Compilation failed: retry
        raise exceptions.CompileException()

def execute_func(function_info):
    ''' executes the function stored in info '''
    try:
        exec(function_info['compiled'], globals())
        # need to remove the compiled version in order to avoid JSON logging issues
        function_info['compiled'] = None
        return function_info
    except:
        raise exceptions.ExecException()
    

# NOTE: Requires Python 3.10+
def exception_handler(e : Exception, verbose, log : logger.Logger):
    match e:
        case exceptions.JSONException():
            if verbose:
                log.log('[Pythoness] JSON parsing failed.')
            to_add = "of a JSON parsing error"

        case exceptions.CompileException():
            if verbose:
                log.log('[Pythoness] Compilation failed.')
            to_add = "of a compilation error"
        
        case exceptions.ExecException():
            if verbose:
                log.log('[Pythoness] Executing the function failed')
            to_add = "of an execution error"

        case exceptions.TypeCompatibilityException():
            if verbose:
                log.log('[Pythoness] The generated function is incompatible with the spec.')
            to_add = "the types of the function and spec were incompatible"

        case timeout.TimeoutException():
            # should timeout be verbose or always included?
            log.log("[Pythoness] Timed out.")
            to_add = "it timed out"

        case exceptions.TestsException():
            if verbose:
                log.log(f"[Pythoness] This test failed to execute properly: {e}")
            to_add = f"this test failed to execute properly: {e}"

        case exceptions.TestsFailedException():
            if verbose:
                log.log(f"[Pythoness] The following tests failed: {e}")
            to_add = f"the following tests failed: {e}"

        case _:
            log.log(f"[Pythoness] Unknown error: {e}")
            to_add = "of an unknown error"

    prompt = f"        Your previous attempt failed because {to_add}. Try again."
    return prompt

