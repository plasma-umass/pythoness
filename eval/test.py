import re


def remove_function_definition(llm_code: str, func_name: str):
    # Improved regex pattern to handle multi-line function headers
    pattern = rf"^\s*def\s+{re.escape(func_name)}\s*\([^)]*\)\s*->?\s*[^:]*:\s*\n"

    # Replace the matched function header with an empty string
    llm_code = re.sub(pattern, "", llm_code, flags=re.MULTILINE)

    return llm_code


# Example test case
llm_code = """
def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    print("Hello, World!")

def another_function():
    pass
"""

func_name = "findMedianSortedArrays"
new_code = remove_function_definition(llm_code, func_name)

print("Modified Code:\n", new_code)
