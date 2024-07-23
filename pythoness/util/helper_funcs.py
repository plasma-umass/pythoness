from . import assistant
from . import logger
from . import exceptions
from . import timeout
import ast_comments as ast
import inspect
import traceback
import json
import os
import inspect



# testing accesses the globals which I then remove

def get_function_info(func):
    """ Gets function info from the provided spec """
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
    ret['return_type'] = func.__annotations__.get('return', '')
    return ret

def get_class_names(func):
    qualname_parts = func.__qualname__.split('.')
    class_names = [part for part in qualname_parts[:-1]]

    return class_names

def ast_class_body_search(cls : ast.ClassDef, func):
    for node in cls.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func.__name__:
            return func
    return
            

def ast_class_search(func, cur_class, class_names):
    if len(class_names) == 0:
        # grab the correct func
        for node in cur_class.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func.__name__:
                return (cur_class, cur_class.body.index(node))
    else:
        search_for = class_names[0]
        for node in cur_class.body:
            if isinstance(node, ast.ClassDef) and node.name == search_for:
                return ast_class_search(func, class_names[1::])
    return None


def replace_func(func, function_def):
    """ Replaces the spec in the file with the generated function def """

    file_name = os.path.abspath(inspect.getfile(func))
    
    with open(file_name, 'r') as file:
        source = file.read()
    tree = ast.parse(source)
    # Find the function with the given name and replace it with the new function.

    func_class_list = get_class_names(func)
    if func_class_list:
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef)) and node.name == func_class_list[0]:
                cls, index = ast_class_search(func, node, func_class_list[1::])
                fn_body = ast.parse(function_def).body
                cls.body[index] = fn_body
                break
    else:
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func.__name__:
                node_index = tree.body.index(node)
                fn_body = ast.parse(function_def).body
                tree.body[node_index] = fn_body
                break

    new_source = ast.unparse(tree)
    # Update the file.
    with open(file_name, 'w') as f:
        f.write(new_source)

def database_compile(function_info, function_def, *args, **kwargs):
    """ Compiles and executes a function with information from the CodeDatabase """

    compiled = compile(function_def, 'generated_func', 'exec')
    exec(compiled, function_info['globals'])
    fn = function_info['globals'][function_info['function_name']]
    # need to remove the new function from the global namespace that exec put it in


    return fn(*args, **kwargs)

def get_all_classed_funcs(cls, target_func):
    ret = []
    nested = inspect.getmembers(cls, inspect.isclass)
    if nested:
        for nest in nested:
            if nest[0] != '__class__':
                ret += get_all_classed_funcs(nest[1], target_func)
    func_list = inspect.getmembers(cls, inspect.isfunction)
    for func in func_list:
        if func != target_func:
            ret.append(func)
    return ret

def setup_info(function_info, func, string, prompt):
    """ Creates the function_info dictionary """
    # func_list = []
    # for cls in func.__globals__.values():
    #     if inspect.isclass(cls):
    #         func_list += get_all_classed_funcs(cls, func)
    # for key, value in func_list:
    #     func.__globals__[value.__qualname__] = value


    function_info.update({'spec': string, 'retries': 0, 'function_def': None, 'compiled': None, 'globals': func.__globals__, 'original_prompt': prompt, 'globals_no_print' : []})
    return function_info

def parse_func(function_info, client: assistant.Assistant, prompt, verbose, log: logger.Logger):
    """ Using Assistant, queries the LLM and places returned information in function_info """
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
    """ Compiles the function_def stored in info """
    try:
        compiled = compile(function_info['function_def'], 'generated_func', 'exec')
        function_info['compiled'] = compiled
        return function_info
    except:
        # Compilation failed: retry
        raise exceptions.CompileException()

def execute_func(function_info):
    """ Executes the function stored in info """
    try:
        exec(function_info['compiled'], function_info['globals'])
        # need to remove the compiled version in order to avoid JSON logging issues
        function_info['compiled'] = None
        return function_info
    except:
        raise exceptions.ExecException()
# NOTE: Requires Python 3.10+

def exception_handler(e: Exception, verbose: bool, log: logger.Logger):
    """ Handles all exceptions that may occur in the main loop of pythoness """
    match e:
        case exceptions.JSONException():
            if verbose:
                log.log('[Pythoness] JSON parsing failed.')
            to_add = 'of a JSON parsing error'
        case exceptions.CompileException():
            if verbose:
                log.log('[Pythoness] Compilation failed.')
            to_add = 'of a compilation error'
        case exceptions.ExecException():
            if verbose:
                log.log('[Pythoness] Executing the function failed')
            to_add = 'of an execution error'
        case exceptions.TypeCompatibilityException():
            if verbose:
                log.log('[Pythoness] The types of the generated function are incompatible with the spec.')
            to_add = 'the types of the function and spec were incompatible'
        case exceptions.DefaultMismatchException():
            if verbose:
                log.log('[Pythoness] The generated function has mismatching default arguments.')
            to_add = 'the default values of the function and spec were incompatible'
        case timeout.TimeoutException():
            # should timeout be verbose or always included?
            log.log('[Pythoness] Timed out.')
            to_add = 'it timed out'
        case exceptions.TestsException():
            if verbose:
                log.log(f'[Pythoness] This test failed to execute properly: {e}')
            to_add = f'this test failed to execute properly: {e}'
        case exceptions.TestsFailedException():
            if verbose:
                log.log(f'[Pythoness] The following tests failed: {e}')
            to_add = f'the following tests failed: {e}'
        case KeyError():
            to_add = "the function or method failed to execute. Ensure that only a single function or method is defined"
        case _:
            if verbose:
                log.log(f'[Pythoness] Unknown error: {type(e)} {e}')
            to_add = f'of an unknown error: {type(e)} {e}'
    if verbose:
        log.log(f"{type(e)} {e}")
        traceback.print_exception(e)
    prompt = f'        Your previous attempt failed because {to_add}. Try again.'
    return prompt