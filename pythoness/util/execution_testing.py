from . import helper_funcs


def add_execution_testing(
    function_info: dict,
    property_tests: list,
    cdb,
) -> dict:
    for p in property_tests:
        print(p)

    function_info["function_def"] = _execution_decorator(function_info, property_tests)
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


def _execution_decorator(function_info: dict, property_tests: list) -> str:
    """Executes the function stored in info"""
    # Create the wrapper function code
    name = function_info["function_name"]
    renamed_tests = [s.replace(name, "func") for s in property_tests]

    wrapped_code = [
        f"def decorator(func):",
        f"  def wrapper(*args, **kwargs):",
        f"    result = func(*args, **kwargs)",
        f"    print('Result of running func:', result)",
        f"    return result",
        f"  return wrapper",
        f"\n@decorator\n{function_info['function_def']}",
    ]

    return "\n".join(wrapped_code)
