from . import helper_funcs


def add_execution_testing(
    function_info: dict,
    cdb,
) -> dict:

    function_info["function_def"] = execution_decorator(function_info)
    function_info = helper_funcs.compile_func(function_info)
    function_info = helper_funcs.execute_func(function_info)

    cdb.delete_code(
        function_info["original_prompt"],
    )
    cdb.insert_code(
        function_info["original_prompt"],
        function_info["function_def"],
    )
    return function_info


def execution_decorator(function_info: dict) -> str:
    """Executes the function stored in info"""
    # Create the wrapper function code
    wrapped_code = [
        f"def decorator(func):",
        f"  def wrapper(*args, **kwargs):",
        f"    result = func(*args, **kwargs)",
        f"    print('Running execution tests...')",
        f"    return result",
        f"  return wrapper",
        f"\n@decorator\n{function_info["function_def"]}",
    ]

    return "\n".join(wrapped_code)
