from . import exceptions
from . import logger
from collections.abc import Generator
from typing import Callable
from hypothesis import example, given
from hypothesis.strategies import *
import textwrap
import logging
import inspect
import traceback
import sys

def validate_types(func : Callable, fn : Callable):
    ''' Validates that the types of func (spec) and fn (produced) are equal '''
    f_sig = inspect.signature(func)
    g_sig = inspect.signature(fn)

    # if the lengh is different, it doesn't match
    if len(f_sig.parameters) != len (g_sig.parameters):
        raise exceptions.TypeCompatibilityException()
    
    for f_param, g_param in zip(f_sig.parameters.values(), g_sig.parameters.values()):
        f_type = f_param.annotation
        g_type = g_param.annotation

        f_default = f_param.default
        g_default = g_param.default

        # if they are both typed and not the same type, they don't match
        if (f_type != inspect.Parameter.empty and g_type != inspect.Parameter.empty) and (f_type != g_type):
            raise exceptions.TypeCompatibilityException()
        
        # make sure the defaults are exactly equal
        if (f_default != g_default):
            raise exceptions.DefaultMismatchException

    f_return_type = f_sig.return_annotation
    g_return_type = g_sig.return_annotation
    
    # same is true for returns
    if (f_return_type != inspect.Parameter.empty and g_return_type != inspect.Parameter.empty) and (f_return_type != g_return_type):
        raise exceptions.TypeCompatibilityException()

    return
    

def validate_tests(function_info, tests, log : logger.Logger):
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
            log.log('Falsifying example is ' + falsifying_example)
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
    ''' Obtain the values of the parameters for which the hypothesis test is failing.'''
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
    ''' Creates hypothesis tests '''
    if isinstance(t[0], dict):
        assertion = t[1]
        given_input = ','.join(t[0].values())
        parameter_input = ','.join(list(t[0].keys()))

        hypothesis_test = textwrap.dedent(f"""
        from hypothesis import example, given
        from hypothesis.strategies import *
        try:
            @given({given_input})
            def test({parameter_input}):
                assert({assertion})                                
            test()
        except KeyboardInterrupt:
            pass
            """)

    else:
        raise Exception(f'The following test does not have a dictionary in it ({t}). Please use correct syntax')
    return compile(hypothesis_test, '<string>', 'exec')
