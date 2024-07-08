from . import assistant
from . import logger
from . import exceptions
from . import timeout
import inspect
import json
import ast_comments as ast

def get_function_info(func):
    ''' Gets function info from the provided spec '''
    ret = {}
    ret['function_name'] = func.__name__
    ret['arg_types'] = []
    f_sig = inspect.signature(func)

    for param in f_sig.parameters.values():
        spec_list = []
        spec_list.append(f'Name: {param.name}')
        if param.annotation is not inspect.Parameter.empty:
            spec_list.append(f'Type: {param.annotation}')
        if param.default is not inspect.Parameter.empty:
            spec_list.append(f'Default: {param.default}')

        ret['arg_types'].append(spec_list)

    ret['return_type'] = func.__annotations__.get('return', "")
    return ret

def replace_func(frame, function_name, function_def):
    ''' Replaces the spec in the file with the generated function def '''
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
    ''' Executes the function stored in info '''
    try:
        exec(function_info['compiled'], globals())
        # need to remove the compiled version in order to avoid JSON logging issues
        function_info['compiled'] = None
        return function_info
    except:
        raise exceptions.ExecException()
    

# NOTE: Requires Python 3.10+
def exception_handler(e : Exception, verbose, log : logger.Logger):
    ''' Handles all exceptions that may occur in the main loop of pythoness '''
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
                log.log('[Pythoness] The types of the generated function are incompatible with the spec.')
            to_add = "the types of the function and spec were incompatible"

        case exceptions.DefaultMismatchException():
            if verbose:
                log.log('[Pythoness] The generated function has mismatching default arguments.')
            to_add = "the default values of the function and spec were incompatible"

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

