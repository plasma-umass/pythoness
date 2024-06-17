from .assistant import Assistant
from .database import CodeDatabase
from .helper_funcs import *
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
