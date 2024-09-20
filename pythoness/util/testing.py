from . import exceptions
from . import logger
from . import unittesting_helpers
from collections.abc import Generator
from typing import Callable
from hypothesis import example, given
from hypothesis.strategies import *
import textwrap
import logging
import inspect
import traceback
import sys
import unittest
import io
import os
import ast

def validate_types(func : Callable, fn : Callable, function_info : dict) -> None:
    """Validates that the types of func (spec) and fn (produced) are equal"""
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
    
    if is_def_within_func(fn, function_info):
        raise exceptions.DefWithinException()

    return

def is_def_within_func(fn, function_info : dict) -> None:
    """Returns True if fn contains a function or class definition within it"""
    
    tree = ast.parse(function_info['function_def'])

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == fn.__name__:
            for node in node.body:
                if isinstance(node, ast.ClassDef) or isinstance(node, ast.FunctionDef):
                    return True
        
    return False

def cleanup_tests(suite : unittest.TestSuite) -> unittest.TestSuite:
    """Removes tests that failed to load from a unittest.TestSuite"""
    cleaned_suite = unittest.TestSuite()
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            # Recursively clean nested test suites
            cleaned_subsuite = cleanup_tests(test)
            cleaned_suite.addTests(cleaned_subsuite)
        elif isinstance(test, unittest.TestCase):
            # Check if the test case is a failed loader type
            if not isinstance(test, unittest.loader._FailedTest):
                cleaned_suite.addTest(test)

    return cleaned_suite


def validate_tests(function_info : dict, tests : list, log : logger.Logger) -> None:
    """Validates that all provided tests pass, prints out which ones, if any, fail"""
    failing_tests = []
    failing_unittests = None

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for t in tests:
        try:
            if isinstance(t, tuple):
                compiled_hypothesis_test = create_hypothesis_test(t)
                exec(compiled_hypothesis_test, function_info["globals"])
            # unittest-ing
            elif inspect.ismodule(t):
                suite.addTest(loader.loadTestsFromModule(t))
            elif type(t) == type and issubclass(t, unittest.TestCase):
                suite.addTest(loader.loadTestsFromTestCase(t))
            elif isinstance(t, unittest.TestSuite):
                suite.addTest(t)
            elif isinstance(t, str):
                # at this point, there should be no loading errors
                # TODO: maybe print something out if there is one? Throw an error?
                # just clear it out now just in case
                if not eval(t, function_info["globals"]):
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
                # Convert the dict in first element of tuple to string
                # and add this newly modified tuple to failing_tests
                new_l = list(t)
                string_input = str(t[0])
                new_l[0] = string_input
                new_t = tuple(new_l)
                failing_tests.append(new_t)
            else:
                failing_tests.append(t)
        except:
            raise exceptions.TestsException(t)

    if suite.countTestCases() > 0:
        captured_output = io.StringIO()
        suite = cleanup_tests(suite)
        # result = unittest.main(testRunner=unittest.TextTestRunner(stream=captured_output), defaultTest='suite', exit=False) 
        runner = unittesting_helpers.CustomTextTestRunner(stream=captured_output)
        result = runner.run(suite)
        
        if not result.wasSuccessful():
            # failing_unittests = captured_output.getvalue()
            failing_unittests = captured_output.getvalue()
            if "Exception: Maximum number of retries exceeded " in failing_unittests:
                raise exceptions.MaxRetriesException(f'Maximum number of retries exceeded.')
    if len(failing_tests) > 0 or failing_unittests:
        # At least one test failed. Retry.
        raise exceptions.TestsFailedException(failing_tests, failing_unittests)
    return





def get_falsifying_example(exception_info: Generator[str, None, None]) -> str:
    """Obtain the values of the parameters for which the hypothesis test is failing."""
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

def create_hypothesis_test(t : tuple):
    """Creates hypothesis tests"""
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

