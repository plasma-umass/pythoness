from . import exceptions
from . import logger
from . import unittesting_helpers
from . import assistant
from . import prompt_helpers
from collections.abc import Generator
from typing import Callable
from hypothesis import example, given
from hypothesis.strategies import *
import logging
import inspect
import traceback
import sys
import unittest
import json
import io
import ast
import re


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


def generate_user_tests(
    function_info: dict,
    tests: list,
    test_descriptions: list,
    client: assistant.Assistant,
    log: logger.Logger,
    verbose: bool,
    llm_tests: bool,
) -> list:
    """Generates tests from the user's specifications and descriptions, and any additional tests authored by LLM"""

    # List of all tests, including code for property tests
    all_tests = []
    # For runtime testing - list of property assertions
    property_tests = []
    # So that LLM doesn't generate dups
    generated_tests = ""
    ptests_count = 1

    # Generate specified property-based tests
    if tests:
        for t in tests:
            try:

                if isinstance(t, tuple):
                    result = client.fork().query(
                        prompt_helpers.specified_property_prompt(t, ptests_count)
                    )
                    ptests_count += 1
                    test = json.loads(result)["code"]
                    all_tests.append(("property", test))
                    property_tests.append(test)
                    generated_tests += test + "\n\n"
                    if verbose:
                        log.log(f"[Pythoness] Synthesized Hypothesis test:\n{test}")
                else:
                    all_tests.append(t)
            except:
                if verbose:
                    log.log(f"[Pythoness] Failed to generate Hypothesis test: {t}")

    # Generate property-based tests from NL descriptions
    if test_descriptions:
        for td in test_descriptions:
            try:
                result = client.fork().query(
                    prompt_helpers.nl_property_prompt(
                        function_info["function_name"], td, ptests_count
                    )
                )
                ptests_count += 1
                test = json.loads(result)["code"]
                all_tests.append(("property", test))
                property_tests.append(test)
                generated_tests += test + "\n\n"
                if verbose:
                    log.log(f"[Pythoness] Synthesized Hypothesis test:\n{test}")
            except:
                if verbose:
                    log.log(f"[Pythoness] Failed to generate Hypothesis test: {td}")

    if llm_tests:
        all_tests, property_tests = generate_llm_tests(
            function_info,
            client,
            log,
            verbose,
            all_tests,
            property_tests,
            ptests_count,
            generated_tests,
        )

    return all_tests, property_tests


def generate_llm_tests(
    function_info: dict,
    client: assistant.Assistant,
    log: logger.Logger,
    verbose: bool,
    llm_tests: bool,
    all_tests: list = [],
    property_tests: list = [],
    ptests_count: int = 1,
    generated_tests: str = "",
) -> list:
    """Generates tests from the user's specifications and descriptions, and any additional tests authored by LLM"""
    # Query LLM for additional property-based tests
    if not llm_tests:
        return all_tests, property_tests

    try:
        prompt = prompt_helpers.llm_new_property_prompt(
            function_info["function_name"], generated_tests[:-2], ptests_count
        )
        result = client.fork().query(prompt)
        code = json.loads(result)["code"]
        new_tests = code.split("\n\n")
        for nt in new_tests:
            all_tests.append(("property", nt))
            property_tests.append(nt)
            if verbose:
                log.log(f"[Pythoness] LLM-Synthesized Hypothesis test:\n{nt}")
    except:
        if verbose:
            log.log(f"[Pythoness] Failed to generate additional property-based tests.")

    # Query LLM for additional unit tests
    try:
        existing_tests = [t for t in all_tests if isinstance(t, str)]
        existing_tests = "\n\n".join(existing_tests)
        existing_tests += "\n\n" + generated_tests
        prompt = prompt_helpers.llm_new_unit_prompt(
            function_info["function_name"], existing_tests[:-2]
        )
        result = client.fork().query(prompt)
        new_tests = json.loads(result)["code"]
        new_tests = re.split(r"\n+", new_tests)
        new_tests = [s for s in new_tests if s]
        all_tests.append(new_tests)

        if verbose:
            log.log(f"[Pythoness] LLM-Synthesized Unit tests:\n{new_tests}")
    except Exception as e:
        if verbose:
            log.log(f"[Pythoness] Failed to generate additional unit tests.")

    return all_tests, property_tests


def validate_tests(
    function_info: dict,
    all_tests: list,
    log: logger.Logger,
    verbose: bool,
) -> None:
    """Validates that all provided tests pass, prints out which ones, if any, fail"""
    failing_tests = []
    failing_unittests = None
    invalid_test_indices = []

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Load hypothesis modules
    exec("from hypothesis import given, strategies as st", function_info["globals"])

    # Store test names for easy failure reporting
    test_names = []
    for t in all_tests:
        if isinstance(t, tuple):
            match = re.search(r"def (\w+)\(", t[1])
            if match:
                test_names.append(match.group(1))
        else:
            test_names.append(t)

    # Run user-specified tests
    for i, t in enumerate(all_tests):
        try:
            if isinstance(t, tuple):
                compile(t[1], "<string>", "exec")
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
                    failing_tests.append(test_names[i])

        except AssertionError as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
            exception_info = tb.format_exception_only()
            line_number = 0
            falsifying_example = get_falsifying_example(exception_info)
            for exception_line in exception_info:
                logging.DEBUG(str(line_number) + " " + exception_line)
                line_number += 1
            log.log("Falsifying example is " + falsifying_example)
            print(e)
            failing_tests.append(test_names[i])
        except SyntaxError as e:
            invalid_test_indices.append(i)
            if verbose:
                log.log(
                    f"Test {test_names[i]} contains syntax errors and will be discarded."
                )
        except:
            raise exceptions.TestsException(t)

    # Remove invalid tests from tests lists
    for i in reversed(invalid_test_indices):
        all_tests.pop(i)
        test_names.pop(i)

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
