from . import exceptions
from . import logger
from . import unittesting_helpers
from . import assistant
from . import prompt_helpers
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

import bigO
import re


def validate_types(func: Callable, fn: Callable, function_info: dict) -> None:
    """Validates that the types of func (spec) and fn (produced) are equal"""
    f_sig = inspect.signature(func)
    g_sig = inspect.signature(fn)

    # if the lengh is different, it doesn't match
    if len(f_sig.parameters) != len(g_sig.parameters):
        print("Length different.", f_sig, g_sig)
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
            print("Not same type", f_sig, g_sig)
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
        print("Not same return type", f_sig, g_sig)
        raise exceptions.TypeCompatibilityException()

    # if is_def_within_func(fn, function_info):
    #     raise exceptions.DefWithinException()

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
    llm_unit: bool,
    llm_prop: bool,
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

    all_tests, property_tests = generate_llm_tests(
        function_info,
        client,
        log,
        verbose,
        llm_unit,
        llm_prop,
        llm_tests,
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
    llm_unit: bool,
    llm_prop: bool,
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

    if llm_prop:
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
                log.log(
                    f"[Pythoness] Failed to generate additional property-based tests."
                )

    # Query LLM for additional unit tests
    if llm_unit:
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
                log.log(f"Test {i} contains syntax errors and will be discarded.")
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


def validate_runtime(
    function_info: dict,
    generate_func: Callable,
    length_func: Callable,
    range: tuple,
    time_bound: str | None,
    mem_bound: str | None,
    log: logger.Logger,
    verbose: bool,
):
    """Uses generate_func to run check() a single time and verify time_bound/mem_bound"""

    fn = function_info["globals"][function_info["function_name"]]

    # checked_fn is a wrapper around the checked and tracked function.
    # don't put f in the global scope, so recursive calls don't trigger
    # additional tracking steps.
    checked_fn = bigO.bounds(
        length_func, time=time_bound, mem=mem_bound, interval=None
    )(fn)

    lower_bound, upper_bound = range

    sample_size = 10

    sample = np.linspace(
        lower_bound,
        upper_bound - 1,
        min(sample_size, upper_bound - lower_bound),
        dtype=int,
    )

    # make it be exactly sample_size samples...
    while len(sample) < sample_size:
        sample = np.append(sample, sample)
    sample = sample[0:sample_size]

    with log("[Pythoness] Validating runtime..."):

        with log("Running bigO checks..."):
            for i, num in enumerate(sample):
                if verbose:
                    log.log(f"iter: {i} len: {num}")

                args, kwargs = generate_func(num)
                checked_fn(*args, **kwargs)

        with log("Checking bigO results..."):
            try:
                results = bigO.bigO.check(fn)
                for result in results:
                    if not result.success:
                        raise exceptions.BigOException(result.message)
            except Exception as e:
                log.log("Exception during bigO check -- continuing: ", e)

    # Don't do this here -- we don't want to keep the checked version around right now...
    # function_info["globals"][function_info["function_name"]] = checked_fn


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

    The function must take 'len' as an argument, where 'len' is an int that describes how long the input should be.

    Only produce output that can be parsed as JSON and only return a single function. Use this template 
    for your response:
    
        def generator_func(len):
            ...
            return ([...], {"{...}"})
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
