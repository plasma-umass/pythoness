from .assistant import Assistant
from .database import CodeDatabase
import textwrap
import json
import logging
import inspect
import ast_comments as ast
import traceback
import sys
from hypothesis import example, given
from hypothesis.strategies import *
from collections.abc import Generator
from functools import wraps
import __main__ as main
from typing import Callable
# never used



# TODO: Add history functionality (requires a prompt to be written)
# TODO: Fix assistant functionality
# TODO: Fix writing to files
# TODO: Clean up this code
# TODO: Add flags
# TODO: Add more examples


















def is_interactive():
    if not hasattr(main, '__file__'):
        # executed interactively (e.g. at the CLI or in a Jupyter notebook)
        return True
    else:
        # executed non-interactively (executing a script)
        return False
# TODO: look through this again

def is_type_compatible(f: Callable, g: Callable) -> bool:
    f_sig = inspect.signature(f)
    g_sig = inspect.signature(g)
    # Check number of parameters
    if len(f_sig.parameters) != len(g_sig.parameters):
        # if debug_print:
        print('mismatch in number of parameters')
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
            # if not issubclass(type(None), g_type):
            #    return False
        if not issubclass(g_type, f_type) and (not issubclass(f_type, g_type)):
            # if debug_print:
            print(f'subclass mismatch: f: {f_type}, g: {g_type}')
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
            # if debug_print:
            print('subclass issue with return types')
            return False
    if not issubclass(g_return_type, f_return_type) and (not issubclass(f_return_type, g_return_type)):
        # if debug_print:
        print('second subclass issue with return types')
        return False
    return True

def prep_tests(tests):
    final_tests = []
    for t in tests:
        # what's the difference in tuple tests and string tests?
        if isinstance(t, tuple):
            final_tests.append(t[1])
        elif isinstance(t, str):
            final_tests.append(t)
        else:
            pass
    # note: pythoness originally has a different string
    test_string = '\n'.join(final_tests)
    prompt_string = f'\n        The function should pass the following tests:\n        {test_string}\n    '
    return prompt_string

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

def compile_func_a(function_def, function_info, *args, **kwargs):
    compiled = compile(function_def, '<string>', 'exec')
    exec(compiled, globals())
    fn = globals()[function_info['function_name']]
    return fn(*args, **kwargs)

def parse_func(client: Assistant, prompt, history, stats):
    # NOTE: we do not store the confidence level anywhere
    # return stats with updated values on failure
    # return function_def and json otherwise
    # TODO: I don't remember what to call this, I think I need client
    result = client._test_complete(prompt, history)
    try:
        the_json = json.loads(result)
    except:
        # JSON parse failure: retry
        stats['parse_failures'] += 1
        print('JSON parsing failed.')
        return stats
    function_def = the_json['code']
    confidence = float(the_json['confidence'])
    print('Synthesized function\n', function_def)
    print('Confidence: \n', confidence)
    if confidence < stats['min_confidence']:
        stats['confidence_failures'] += 1
        print(f'Confidence level {confidence} too low (below {stats['min_confidence']}).')
        return stats
    stats['function_def'] = function_def
    # need to return function def
    return stats

def compile_func_b(stats):
    try:
        compiled = compile(stats['function_def'], '<string>', 'exec')
        stats['compiled'] = compiled
        return stats
    except:
        # Compilation failed: retry
        stats['compilation_failures'] += 1
        print('Compilation failed.')
        stats['function_def'] = None
        return stats

def execute_func(stats):
    try:
        exec(stats['compiled'], globals())
        # TODO: compiled functions break JSON, need to rethink this
        stats['compiled'] = None
        return stats
    except:
        print('Executin the function failed')
        stats['exectution_failures'] += 1
        stats['function_def'] = None
        return stats

def validate_types(stats, func, fn):
    if not is_type_compatible(func, fn):
        stats['type_incompatibility failures'] += 1
        # Function types don't validate: retry
        print('The generated function is incompatible with the spec.')
        stats['function_def'] = None
    return stats

def validate_tests(tests, failing_tests, stats):
    for t in tests:
        try:
            if isinstance(t, tuple):
                compiled_hypothesis_test = create_hypothesis_test(t)
                exec(compiled_hypothesis_test, globals())
            elif not eval(t):
                failing_tests.add(t)
        except AssertionError:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
            exception_info = tb.format_exception_only()
            line_number = 0
            falsifying_example = get_falsifying_example(exception_info)
            for exception_line in exception_info:
                logging.DEBUG(str(line_number) + ' ' + exception_line)
                line_number += 1
            print('Falsifying example is ' + falsifying_example)
            if isinstance(t, tuple):
                #Convert the dict in first element of tuple to string
                #and add this newly modified tuple to failing_tests
                new_l = list(t)
                string_input = str(t[0])
                new_l[0] = string_input
                new_t = tuple(new_l)
                failing_tests.add(new_t)
            else:
                failing_tests.add(t)
        except:
            raise Exception(f'This test failed to execute properly: {t}')
    if len(failing_tests) > 0:
        stats['test_failures'] += 1
        stats['num_tests_failed'] += len(failing_tests)
        # At least one test failed. Retry.
        print(f'[Pythoness] Tests failed: {failing_tests}')
        stats['function_def'] = None
    return (stats, failing_tests)














def spec(string, replace=False, tests=None, max_retries=3, verbose=False, min_confidence=0.7, output=False, regenerate=False):
    # regenerate means ignore code in the DB

    def decorator(func):
        cached_function = None
        cdb = CodeDatabase('pythoness-cache.db')

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal cdb, cached_function
            client = Assistant('')
            function_info = get_function_info(func, *args, **kwargs)
            # do I need the \'s?

            prompt = f"""

            Produce a JSON object with code for a Python function
            named {function_info['function_name']} that performs the following task as
            a field \"code\".  Report your confidence that this code
            performs the task as a number between 0 and 1, as a field
            \"confidence\".  Only produce output that can be parsed as
            JSON.
            
            Task:
            {textwrap.dedent(string)}

            Include a docstring containing the task description above
            (without the word "Task:").  The function should be
            entirely self-contained, with all imports, code, and data
            required for its functionality.  """


            if tests:
                prompt += prep_tests(tests)


            prompt += f"""
            The function should have the following argument types and return type:
            
            Arguments: {function_info['arg_types']}
            Return type: {function_info['return_type']}
            """


            print('Prompt:\n', prompt)
            function_def = cdb.get_code(prompt)
            if function_def:
                return compile_func_a(function_def, function_info, *args, **kwargs)
            stats = {}
            stats['spec'] = string
            # add prompt here?
            # unnecessary?
            stats['function_name'] = function_info['function_name']
            stats['tests_provided'] = json.dumps(tests, indent=2)
            stats['num_tests_failed'] = 0
            stats['retries'] = 0
            stats['successes'] = 0
            stats['parse_failures'] = 0
            stats['execution_failures'] = 0
            stats['below_confidence_level'] = 0
            stats['compilation_failures'] = 0
            stats['type_incompatibility_failures'] = 0
            stats['test_failures'] = 0
            stats['min_confidence'] = min_confidence
            stats['function_def'] = None
            stats['compiled'] = None
            # can't have a set in stats
            failing_tests = set()
            history = []
            while stats['retries'] < max_retries:
                stats['retries'] += 1
                print(f'Attempt number {stats['retries']}.')
                if not function_def:
                    stats = parse_func(client, prompt, history, stats)
                    if not stats['function_def']:
                        continue
                # need 'continue' on failure
                # maybe store stuff in stats
                stats = compile_func_b(stats)
                if not stats['function_def']:
                    continue
                # need 'continue' on failure
                stats = execute_func(stats)
                if not stats['function_def']:
                    continue
                # need 'continue' on failure


                fn = globals()[stats['function_name']]
                stats = validate_types(stats, func, fn)
                if not stats['function_def']:
                    continue
                if tests:
                    test_results = validate_tests(tests, failing_tests, stats)
                    stats = test_results[0]
                    failing_tests = test_results[1]
                    if not stats['function_def']:
                        continue
                stats['successes'] += 1
                logging.info(json.dumps(stats))
                # Validated. Cache the function and persist it
                cached_function = fn
                cdb.insert_code(prompt, stats['function_def'])
                if output:
                    print(stats['function_def'], file=sys.stdout)


                # if selected, replace
                if replace: 
                    import inspect
                    frame = inspect.currentframe()
                    frame = frame.f_back
                    file_name = frame.f_code.co_filename
                    with open(file_name, 'r') as file:
                        source = file.read()
                    tree = ast.parse(source)
                    # Find the function with the given name and replace it with the new function.
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == stats['function_name']:
                            node_index = tree.body.index(node)
                            fn_body = ast.parse(stats['function_def']).body
                            tree.body[node_index] = fn_body
                    new_source = ast.unparse(tree)
                    # Update the file.
                    with open(file_name, 'w') as f:
                        f.write(new_source)
        
                return cached_function(*args, **kwargs)
            # If we got here, we had too many retries.
            logging.info(json.dumps(stats))
            if failing_tests:
                raise Exception(f'Maximum number of retries exceeded ({max_retries}).\nFailing tests: {failing_tests}')
            else:
                raise Exception(f'Maximum number of retries exceeded ({max_retries}).')
        return wrapper
    return decorator














def get_falsifying_example(exception_info: Generator[str, None, None]) -> str:
    """Obtain the values of the parameters for which the hypothesis test is failing.
    """
    assertion_error = False
    result = ''
    for exception_line in exception_info:
        if 'AssertionError' in exception_line:
            assertion_error = True
            break
    if assertion_error:
        input_start = False
        for exception_line in exception_info:
            if ')' in exception_line:
                input_start = False
                continue
            if 'Falsifying example:' in exception_line:
                input_start = True
                continue
            if input_start:
                result = result + exception_line.strip()
    return result

def create_hypothesis_test(t):
    if isinstance(t[0], dict):
        assertion = t[1]
        given_input = ','.join(t[0].values())
        parameter_input = ','.join(list(t[0].keys()))
        hypothesis_test = f'\n@given({given_input})\ndef test({parameter_input}):\n    assert({assertion})                                \ntest()\n'
    else:
        raise Exception(f'The following test does not have a dictionary in it ({t}). Please use correct syntax')
    return compile(hypothesis_test, '<string>', 'exec')
logging.basicConfig(filename='pythoness.log', encoding='utf-8', format='%(message)s', level=logging.DEBUG)