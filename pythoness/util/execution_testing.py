from . import assistant
from . import helper_funcs
from . import logger
from . import prompt_helpers
import ast
import astor
import json
import sys


def add_execution_testing(
    function_info: dict,
    property_tests: list,
    client: assistant.Assistant,
    func,
    log: logger.Logger,
    verbose: bool,
    cdb,
) -> dict:
    if property_tests:
        property_tests = "\n".join(property_tests)

    function_info["function_def"] = _execution_decorator(
        function_info, property_tests, client, func, log, verbose
    )

    function_info = helper_funcs.compile_func(function_info)
    function_info = helper_funcs.execute_func(function_info)

    # Remove and replace the code being stored in the database
    cdb.delete_code(
        function_info["original_prompt"],
    )
    cdb.insert_code(
        function_info["original_prompt"],
        function_info["function_def"],
    )
    return function_info


def _execution_decorator(
    function_info: dict,
    property_tests: str,
    client: assistant.Assistant,
    func,
    log: logger.Logger,
    verbose: bool,
) -> str:
    """Creates the decorator around the generated function that runs runtime tests."""
    name = function_info["function_name"]
    arg_names = [arg.split(": ")[1] for arg, _ in function_info["arg_types"]]
    partial_sig = f"({', '.join(arg_names)})"

    result = client.fork().query(prompt_helpers.runtime_testing_prompt(property_tests))
    code_snippet = json.loads(result)["code"]

    wrapped_code = "\n".join(
        [
            f"def decorator({name}):",
            f"  def wrapper{prompt_helpers.prep_signature(func)}:",
            f"    runtime_result = {name}{partial_sig}",
            f"    print('Result of running {name}:', runtime_result)",
            f"    try:",
            f"      pass",
            f"    except AssertionError:",
            f"      print('Property test failed')",
            f"    return runtime_result",
            f"  return wrapper",
            f"\n@decorator\n{function_info['function_def']}",
        ]
    )

    # Parse wrapper code and LLM result
    wrapper_ast = ast.parse(wrapped_code)
    snippet_ast = ast.parse(code_snippet).body

    # Modify the AST
    class PassReplacer(ast.NodeTransformer):
        def visit_Pass(self, node):
            return snippet_ast

    wrapper_ast = PassReplacer().visit(wrapper_ast)

    return astor.to_source(wrapper_ast)
