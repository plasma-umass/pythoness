from . import exceptions
from . import logger
from . import unittesting_helpers
from . import assistant
from collections.abc import Generator
from typing import Callable
from hypothesis.strategies import *
import logging
import inspect
import traceback
import sys
import unittest
import json
import io
import ast
import random
import numpy as np

from bigO import check



def validate_types(func: Callable, fn: Callable, function_info: dict) -> None:
    """Validates that the types of func (spec) and fn (produced) are equal"""
    f_sig = inspect.signature(func)
    g_sig = inspect.signature(fn)

    # if the lengh is different, it doesn't match
    if len(f_sig.parameters) != len(g_sig.parameters):
        raise exceptions.TypeCompatibilityException()

    for f_param, g_param in zip(f_sig.parameters.values(), g_sig.parameters.values()):
        f_type = f_param.annotation
        g_type = g_param.annotation

        f_default = f_param.default
        g_default = g_param.default

        # if they are both typed and not the same type, they don't match
        if (
            f_type != inspect.Parameter.empty and g_type != inspect.Parameter.empty
        ) and (f_type != g_type):
            raise exceptions.TypeCompatibilityException()

        # make sure the defaults are exactly equal
        if f_default != g_default:
            raise exceptions.DefaultMismatchException

    f_return_type = f_sig.return_annotation
    g_return_type = g_sig.return_annotation

    # same is true for returns
    if (
        f_return_type != inspect.Parameter.empty
        and g_return_type != inspect.Parameter.empty
    ) and (f_return_type != g_return_type):
        raise exceptions.TypeCompatibilityException()

    if is_def_within_func(fn, function_info):
        raise exceptions.DefWithinException()

    return


def is_def_within_func(fn, function_info: dict) -> None:
    """Returns True if fn contains a function or class definition within it"""

    tree = ast.parse(function_info["function_def"])

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == fn.__name__:
            for node in node.body:
                if isinstance(node, ast.ClassDef) or isinstance(node, ast.FunctionDef):
                    return True

    return False


def cleanup_tests(suite: unittest.TestSuite) -> unittest.TestSuite:
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


def generate_tests(
    function_info: dict,
    tests: list,
    test_descriptions: list,
    client: assistant.Assistant,
    log: logger.Logger,
    verbose: bool,
) -> list:
    tests_to_run = []
    property_tests = []

    # Generate specified property-based tests
    if tests:
        for t in tests:
            try:
                if isinstance(t, tuple):
                    test = generate_hypothesis_test(t, client)
                    tests_to_run.append(("property", compile(test, "<string>", "exec")))
                    property_tests.append(test)
                    if verbose:
                        log.log(f"[Pythoness] Synthesized Hypothesis test:\n{test}")
                else:
                    tests_to_run.append(t)
            except:
                if verbose:
                    log.log(f"[Pythoness] Failed to generate Hypothesis test: {t}")

    # Generate property-based tests from NL descriptions
    if test_descriptions:
        for td in test_descriptions:
            try:
                prompt = f"""Produce a JSON object as a field 'code' with code for a property-based Hypothesis
                test for the {function_info["function_name"]} function with the following description: '{td}'.
                Only produce output that can be parsed as JSON and only produce the Hypothesis test."""
                result = client.query(prompt)
                the_json = json.loads(result)
                test = the_json["code"]
                tests_to_run.append(("property", compile(test, "<string>", "exec")))
                property_tests.append(test)
                if verbose:
                    log.log(f"[Pythoness] Synthesized Hypothesis test:\n{test}")
            except:
                if verbose:
                    log.log(f"[Pythoness] Failed to generate Hypothesis test: {td}")

    # Query LLM for additional tests
    # try:
    #     prompt = f"""Produce a JSON object as a field 'code' with a list of additional tests that have not already been generated to evaluate the correct functionality for the {function_info["function_name"]} function.
    #     These can either be single-line unit tests as code assertions, or the full functions for Hypothesis property-based tests.
    #     Only produce output that can be parsed as JSON."""
    #     result = client.query(prompt)
    #     the_json = json.loads(result)
    #     test_list = the_json["code"]
    #     print(the_json)
    # except:
    #     if verbose:
    #         log.log(f"[Pythoness] Failed to generate any additional tests.")

    # for tllm in test_list:
    #     try:
    #         print("NEW TEST:", tllm)
    #     except:
    #         pass

    return tests_to_run, property_tests


def validate_tests(
    function_info: dict,
    tests: list,
    log: logger.Logger,
) -> None:
    """Validates that all provided tests pass, prints out which ones, if any, fail"""
    failing_tests = []
    failing_unittests = None

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Run user-specified tests
    for t in tests:
        try:
            if isinstance(t, tuple):
                exec(t[1], function_info["globals"])
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
                logging.DEBUG(str(line_number) + " " + exception_line)
                line_number += 1
            log.log("Falsifying example is " + falsifying_example)
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
                raise exceptions.MaxRetriesException(
                    f"Maximum number of retries exceeded."
                )
    if len(failing_tests) > 0 or failing_unittests:
        # At least one test failed. Retry.
        raise exceptions.TestsFailedException(failing_tests, failing_unittests)
    return


def get_falsifying_example(exception_info: Generator[str, None, None]) -> str:
    """Obtain the values of the parameters for which the hypothesis test is failing."""
    assertion_error = False
    result = ""
    for exception_line in exception_info:
        if "AssertionError" in exception_line:
            assertion_error = True
            break
    if assertion_error:
        input_start = False
        for exception_line in exception_info:
            if ")" in exception_line:
                input_start = False
                continue
            if "Falsifying example:" in exception_line:
                input_start = True
                continue
            if input_start:
                result = result + exception_line.strip()
    return result


def generate_hypothesis_test(t: tuple, client: assistant.Assistant):
    """Creates hypothesis tests"""
    prompt = f"""Produce a JSON object as a field 'code' with code for the function declaration for an empty Hypothesis
    test given the range '{t[0]}' on the function input. Only produce output that can be parsed as JSON."""
    result = client.query(prompt)
    the_json = json.loads(result)
    code = the_json["code"]

    # Replace the placeholder 'pass' with the user's assertion
    parts = code.rsplit("pass", 1)
    if len(parts) > 1:
        code = t[1].join(parts)
    return code

def validate_runtime(function_info: dict, generate_func: int, length_func: Callable, range: tuple, time_bound: str, log: logger.Logger, verbose: bool):
    """Uses generate_func to run check() a single time and verify time_bound"""

    function_info["globals"][function_info["function_name"]] = check(length_func, time_bound = time_bound, frequency = 25)(function_info["globals"][function_info["function_name"]])
    
    lower_bound = range[0]
    upper_bound = range[1]

    sample_size = 25

    if sample_size > (upper_bound - lower_bound):
        raise ValueError("Sample size k cannot be greater than the upper bound n.")
    
    sample = np.linspace(lower_bound, upper_bound - 1, sample_size, dtype=int)

    i = 0
    for num in sample:
        if verbose:
            log.log(f"iter: {i} len: {num}")
            i += 1

        args, kwargs = generate_func.__call__(num)
        function_info["globals"][function_info["function_name"]].__call__(*args, **kwargs)    

    return 

# mess with input sizes more and more inputs

def generate_generator_func(
    spec: str,
    main_func: callable,
    function_info: dict,
    model: str,
    log: logger.Logger,
    verbose: bool,
):
    
    client = assistant.Assistant(model=model)

    prompt = f"""   Produce a JSON object as a field 'code' with code for a Python function that generates
    a variety of random inputs. This function must return a tuple of a list, where each element in this list 
    represents a single argument in *args, and a dictionary representing the **kwargs.
    If a list is being included in an argument for *args, *args must be wrapped by an additional list.
    
    The generator must adhere to the following specification:

        {spec}

    The generator is creating input for a function matching this signature:
        {function_info["function_name"]}{inspect.signature(main_func)}:
            ...

    Only produce output that can be parsed as JSON and only return a single function. Use this template 
    for your response:
    
        def generator_func():
            ...
    """

    if verbose:
        log.log(f"[Pythoness] Generating a generator function...")
        log.log(f"[Pythoness] Prompt:\n", prompt)

    result = client.query(prompt)
    the_json = json.loads(result)
    func_def = the_json["code"]

    if verbose:
        log.log("[Pythoness] Synthesized generator function: \n", func_def)
    
    compiled = compile(func_def, "generator_func", "exec")
    exec(compiled, function_info["globals"])

    return function_info["globals"]["generator_func"]