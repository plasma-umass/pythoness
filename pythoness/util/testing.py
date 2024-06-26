from . import exceptions
from collections.abc import Generator
from typing import Callable
from hypothesis import example, given
from hypothesis.strategies import *
import textwrap
import logging
import inspect
import traceback
import sys

debug_print = False

def is_type_compatible(f: Callable, g: Callable) -> bool:
    ''' Checks that f and g are type comptabile '''
    f_sig = inspect.signature(f)
    g_sig = inspect.signature(g)
    # Check number of parameters
    if len(f_sig.parameters) != len(g_sig.parameters):
        if debug_print:
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
            if debug_print:
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
            if debug_print:
                print('subclass issue with return types')
            return False
    if not issubclass(g_return_type, f_return_type) and (not issubclass(f_return_type, g_return_type)):
        if debug_print:
            print('second subclass issue with return types')
        return False
    return True

def validate_types(function_info, func, fn):
    ''' Validates that the types of func (spec) and fn (produced) are equal '''
    if not is_type_compatible(func, fn):
        # Function types don't validate: retry
        raise exceptions.TypeCompatibilityException()
    return function_info

def validate_tests(function_info, tests):
    ''' Validates that all provided tests pass, prints out which ones, if any, fail '''
    failing_tests = []
    for t in tests:
        try:
            if isinstance(t, tuple):
                compiled_hypothesis_test = create_hypothesis_test(t)
                exec(compiled_hypothesis_test, function_info["globals"])
            elif not eval(t, function_info["globals"]):
                failing_tests.append(t)
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
                failing_tests.append(new_t)
            else:
                failing_tests.append(t)
        except:
            raise exceptions.TestsException(t)
    if len(failing_tests) > 0:
        # At least one test failed. Retry.
        raise exceptions.TestsFailedException(failing_tests)
    return


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

        hypothesis_test = textwrap.dedent(f"""
        from hypothesis import example, given
        from hypothesis.strategies import *
        @given({given_input})
        def test({parameter_input}):
            assert({assertion})                                
        test()""")

    else:
        raise Exception(f'The following test does not have a dictionary in it ({t}). Please use correct syntax')
    return compile(hypothesis_test, '<string>', 'exec')
