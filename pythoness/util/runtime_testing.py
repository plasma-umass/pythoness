from . import assistant
from . import helper_funcs
from . import logger
from . import prompt_helpers
import ast
import astor
import json


def add_runtime_testing(
    function_info: dict,
    property_tests: list,
    pythoness_args: str,
    tolerance: float,
    max_runtime: int,
    client: assistant.Assistant,
    func,
    log: logger.Logger,
    verbose: bool,
    cdb,
) -> dict:

    function_info["function_def"] = _runtime_decorator(
        function_info,
        property_tests,
        pythoness_args,
        tolerance,
        max_runtime,
        client,
        func,
        log,
        verbose,
    )

    function_info = helper_funcs.compile_func(function_info)
    function_info = helper_funcs.execute_func(function_info, max_runtime)

    # Remove and replace the code being stored in the database
    cdb.delete_code(
        function_info["original_prompt"],
    )
    cdb.insert_code(
        function_info["original_prompt"],
        function_info["function_def"],
    )
    return function_info


def _runtime_decorator(
    function_info: dict,
    property_tests: str,
    pythoness_args: str,
    tolerance: float,
    max_runtime: int,
    client: assistant.Assistant,
    func,
    log: logger.Logger,
    verbose: bool,
) -> str:
    """Creates the decorator around the generated function that runs runtime tests."""
    name = function_info["function_name"]
    arg_names = [arg.split(": ")[1] for arg, _ in function_info["arg_types"]]
    partial_sig = f"({', '.join(arg_names)})"
    num_properties = len(property_tests)
    if property_tests:
        property_tests = "\n".join(property_tests)

    result = client.fork().query(prompt_helpers.runtime_testing_prompt(property_tests))
    llm_code = json.loads(result)["code"]

    # print(code_snippet)

    wrapped_code = "\n".join(
        [
            f"from functools import wraps\n",
            f"import time\n",
            f"def decorator({name}):",
            f"  iteration = [2] * {num_properties}",
            f"  property_passes = [2] * {num_properties}\n",
            f"  @wraps({name})",
            f"  def wrapper{prompt_helpers.prep_signature(func)}:",
            f"    pass",
            f"    for i in range(len(property_passes)):",
            f"      print(i, property_passes[i], iteration[i])",
            f"      result = property_passes[i] / iteration[i]",
            f"      if result < {tolerance}:",
            # f"        return pythoness.spec{pythoness_args}({name}){partial_sig}",
            f"        assert False",
            f"    pass",
            # f"    print('Properties passed.')",
            f"    return {name}{partial_sig}",
            f"  return wrapper",
            f"\n@decorator\n{function_info['function_def']}",
        ]
    )

    timing_code = ""
    if isinstance(max_runtime, (int, float)):
        timing_code = "\n".join(
            [
                f"start = time.perf_counter_ns()",
                f"result = {name}{partial_sig}",
                f"end = time.perf_counter_ns()",
                f"if (end - start) / 1e6 > {max_runtime}:",
                f"  print('Input exceeded allowed runtime.')",
                f"  return pythoness.spec{pythoness_args}({name}){partial_sig}",
            ]
        )

    # Parse wrapper code and LLM result
    wrapper_ast = ast.parse(wrapped_code)
    llm_ast = ast.parse(llm_code)
    timing_ast = ast.parse(timing_code)

    # Modify the AST to replace code placeholders
    class PassReplacer(ast.NodeTransformer):
        def __init__(self):
            self.which = 0

        def visit_Pass(self, node):
            if self.which == 0:
                self.which = 1
                return llm_ast
            else:
                return timing_ast

    wrapper_ast = PassReplacer().visit(wrapper_ast)

    full_code = ast.unparse(wrapper_ast)

    print(full_code)

    return full_code
