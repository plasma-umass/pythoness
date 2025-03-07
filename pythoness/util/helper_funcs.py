from . import assistant
from . import logger
from . import exceptions
from . import timeout
import ast_comments as ast
import inspect
import json
import os
import textwrap
import time
import traceback

from bigO.bigO import BigOError


def get_function_info(func) -> dict:
    """Gets function info from func"""
    ret = {}
    ret["function_name"] = func.__name__
    ret["arg_types"] = []
    f_sig = inspect.signature(func)
    for param in f_sig.parameters.values():
        spec_list = []
        spec_list.append(f"Name: {param.name}")
        if param.annotation is not inspect.Parameter.empty:
            spec_list.append(f"Type: {param.annotation}")
        if param.default is not inspect.Parameter.empty:
            spec_list.append(f"Default: {param.default}")
        ret["arg_types"].append(spec_list)
    ret["return_type"] = func.__annotations__.get("return", "")
    ret["initial_code"] = inspect.getsource(func)
    return ret


def get_class_names(func) -> list:
    """Gets the list of class names a func is under"""
    qualname_parts = func.__qualname__.split(".")
    class_names = [part for part in qualname_parts[:-1]]
    return class_names


def ast_class_search(func, cur_class_node: ast.ClassDef, class_names: list) -> tuple:
    """Searches the ast and returns the class object and index of the class of func in the ast
    or None if it doesn't exist"""
    if len(class_names) == 0:
        # grab the correct func
        for node in cur_class_node.body:
            if (
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == func.__name__
            ):
                return (cur_class_node, cur_class_node.body.index(node))
    else:
        # grab the next class
        search_for = class_names[0]
        for node in cur_class_node.body:
            if isinstance(node, ast.ClassDef) and node.name == search_for:
                return ast_class_search(func, class_names[1::])
    return None


def replace_func(func, function_def: str) -> None:
    """Replaces the spec in the file with the generated function def"""
    file_name = os.path.abspath(inspect.getfile(func))

    with open(file_name, "r") as file:
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
            if (
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == func.__name__
            ):
                node_index = tree.body.index(node)
                fn_body = ast.parse(function_def).body
                tree.body[node_index] = fn_body
                break

    new_source = ast.unparse(tree)
    # Update the file.
    with open(file_name, "w") as f:
        f.write(new_source)


def database_compile(
    function_info: dict, function_def: str, length_func, time_bound, mem_bound
):
    """Compiles and executes a function with information from the CodeDatabase"""
    compiled = compile(function_def, "generated_func", "exec")
    exec(compiled, function_info["globals"])
    # function_info["globals"][function_info["function_name"]] = check(length_func, time = time_bound, mem=mem_bound)(function_info["globals"][function_info["function_name"]])

    return function_info["globals"][function_info["function_name"]]


def setup_info(function_info: dict, func, string: str, prompt: str) -> dict:
    """Creates the function_info dictionary"""
    function_info.update(
        {
            "spec": string,
            "retries": 0,
            "function_def": None,
            "compiled": None,
            "globals": func.__globals__,
            "original_prompt": prompt,
            "globals_no_print": [],
        }
    )
    return function_info


def parse_func(
    function_info: dict,
    client: assistant.Assistant,
    prompt: str,
    verbose: bool,
    log: logger.Logger,
) -> dict:
    """Using Assistant, queries the LLM and places returned information in function_info"""
    result = client.query(prompt)
    function_info["completion"] = result
    try:
        the_json = json.loads(result)
    except:
        # JSON parse failure: retry
        raise exceptions.JSONException()
    function_def = the_json["code"]
    if verbose:
        log.log("[Pythoness] Synthesized function: \n", function_def)
    function_info["function_def"] = function_def

    return function_info


def compile_func(function_info: dict) -> dict:
    """Compiles the function_def stored in info"""
    try:
        compiled = compile(function_info["function_def"], "generated_func", "exec")
        function_info["compiled"] = compiled
        return function_info
    except:
        # Compilation failed: retry
        raise exceptions.CompileException()


def execute_func(function_info: dict, max_runtime: int) -> dict:
    """Executes the function stored in info"""
    try:
        start = time.perf_counter_ns()
        exec(function_info["compiled"], function_info["globals"])
        end = time.perf_counter_ns()
    except:
        raise exceptions.ExecException()

    time_ns = (end - start) / 1e6
    if isinstance(max_runtime, (int, float)) and time_ns > max_runtime:
        raise exceptions.RuntimeExceededException(time)

    # need to remove the compiled version in order to avoid JSON logging issues
    function_info["compiled"] = None
    return function_info


# NOTE: Requires Python 3.10+
def exception_handler(
    e: Exception,
    verbose: bool,
    log: logger.Logger,
    func,
    related_objs: list,
    no_print: list,
) -> str:
    """Handles all exceptions that may occur in the main loop of Pythoness and returns a new prompt based on that exception"""
    match e:
        case exceptions.JSONException():
            if verbose:
                log.log("[Pythoness] JSON parsing failed.")
            to_add = "of a JSON parsing error."
        case exceptions.CompileException():
            if verbose:
                log.log("[Pythoness] Compilation failed.")
            to_add = "of a compilation error."
        case exceptions.ExecException():
            if verbose:
                log.log("[Pythoness] Executing the function failed")
            to_add = "of an execution error."
        case exceptions.TypeCompatibilityException():
            if verbose:
                log.log(
                    "[Pythoness] The types of the generated function are incompatible with the spec. Ensure the signatures match. "
                )
            to_add = "the types of the function and spec were incompatible."
        case exceptions.DefaultMismatchException():
            if verbose:
                log.log(
                    "[Pythoness] The generated function has mismatching default arguments."
                )
            to_add = "the default values of the function and spec were incompatible."
        case timeout.TimeoutException():
            # should timeout be verbose or always included?
            log.log("[Pythoness] Timed out.")
            to_add = "it timed out."
        case exceptions.TestsException():
            if verbose:
                log.log(f"[Pythoness] This test failed to execute properly: {e}")
            to_add = f"this test failed to execute properly: {e}."
        case exceptions.TestsFailedException():
            if verbose:
                str = ""
                if e.normal_tests_failed:
                    str += f"These tests failed: {e.normal_tests_failed}\n\n"

                if e.unittests_failed:
                    str += f"This was the unittest output, which includes a failure and/or error: \n{e.unittests_failed}"

                log.log(f"[Pythoness] Tests failed.\n\n{str}")

            to_add = "tests failed.\n\n"

            if e.normal_tests_failed:
                to_add += f"The following tests failed: {e.normal_tests_failed}\n\n"
            if e.unittests_failed:
                to_add += f"This was the output from a unittest test suite, which includes a failure and/or error:\n{e.unittests_failed}"

        case exceptions.BigOException():
            if verbose:
                log.log("[Pythoness] Big O check failed.")
                log.log(f"[Pythoness] {e}")
            args = "\n".join(e.args)
            to_add = f"the function has a slower time complexity than specified.  Error message:\n```\n{args}\n```\n"

        case KeyError():
            to_add = "the function or method failed to execute. Ensure that only a single function or method is defined. "

        case exceptions.DefWithinException():
            to_add = f"you added a class or function definition within the generated function.\n\n"
            # to_add += (
            #     f"{prompt_helpers.prep_related_objs(func, related_objs, no_print)}"
            # )
            to_add = textwrap.dedent(to_add)

        # case ValueError():
        #     # time bound error
        #     if verbose:
        #         log.log("[Pythoness] Incorrect time bound.")
        #         log.log(f"{e}")
        #     args = "\n".join(e.args[0].split("\n")[1:6])
        #     to_add = f"the function has a slower time complexity than specified. \n{args}\n```\n"

        case _:
            # if verbose:
            #     log.log(f'[Pythoness] Unknown error: {type(e)} {e}')
            to_add = f"of an error: {type(e)} {e}."
    # if verbose:
    # log.log(f"{type(e)} {e}")
    # traceback.print_exception(e)
    prompt = f"        Your previous attempt failed because {to_add} Try again."

    # print(prompt)

    return prompt
