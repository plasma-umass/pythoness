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


def execution_decorator(info: dict) -> str:
    """Executes the function stored in info"""
    function_code = info["function_def"]
    # Create the wrapper function code
    wrapped_code = [
        # f"import functools",
        # f"import inspect",
        f"def decorator(func):",
        # f"  @functools.wraps(func)",
        f"  def wrapper(*args, **kwargs):",
        f"    result = func(*args, **kwargs)",
        f"    print('Running execution tests...')",
        f"    return result",
        # f"  wrapper.__signature__ = inspect.signature(func)",
        f"  return wrapper",
        f"\n@decorator\n{function_code}",
    ]

    # # Add the original function code after the wrapper
    # wrapped_code.extend(lines)

    # # At the end, return the wrapper function
    # wrapped_code.append("return wrapper")

    # Join all the lines back into a single string
    full_code = "\n".join(wrapped_code)
    return full_code
