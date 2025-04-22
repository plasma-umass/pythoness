import re


def extract_args_for_function(func_name, s):
    # Escape the function name in case it contains regex metacharacters
    pattern = rf"\b{re.escape(func_name)}\s*\((.*?)\)"
    match = re.search(pattern, s)
    if match:
        return match.group(1)
    return None


function_info = "my_function"
s = "Some code here, then my_function(42, 'hello', x+1) appears"

args = extract_args_for_function(function_info, s)
print(args)  # Output: "42, 'hello', x+1"
