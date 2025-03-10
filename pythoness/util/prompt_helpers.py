import inspect
import textwrap
import re
import ast
import os
import unittest
from pythoness.util import symbols


def specified_property_prompt(t: tuple, num: int) -> str:
    """Prompt for LLM to generate Hypothesis function from user-specified property-based tests"""

    return f"""Generate a hypothesis function for a property-based test using the following range {t[0]} and assertion {t[1]}.
Assume you have the following imports:
```
from hypothesis import given, strategies as st
```
Respond in JSON output with a 'code' field, filling in the following function format:
```
@given(...)
def property_test_{num}:
    ...
```"""


def nl_property_prompt(name: str, descrip: str, num: int) -> str:
    """Prompt for LLM to generate Hypothesis function from user-provided NL description of property-based test"""

    return f"""Generate a hypothesis function for a property-based test for {name} using the following description: '{descrip}'.
Assume you have the following imports:
```
from hypothesis import given, strategies as st
```
Respond in JSON output with a 'code' field, filling in the following function format:
```
@given(...)
def property_test_{num}:
    ...
```"""


def llm_new_property_prompt(name: str, existing: str, num: int) -> str:
    """Prompt for LLM to generate new Hypothesis functions based off of existing list"""

    return f"""Generate hypothesis functions for property-based tests to evaluate the correct behavior of {name}.
Assume you have the following imports:
```
from hypothesis import given, strategies as st
```
Respond in JSON output with a 'code' field, filling in the following functions list format:
```
@given(...)
def property_test_{num}:
    assert ...

@given(...)
def property_test_{num + 1}:
    assert ...

# Continue for as many or as few tests as needed
```
Here is a list of existing property-based tests. Do not generate any property-based tests that are functionally equivalent to them:
```
{existing}
```"""


def llm_new_unit_prompt(name: str, existing: str) -> str:
    """Prompt for LLM to generate new unit tests based off of existing list"""

    return f"""Generate simple unit tests to evaluate the correct behavior of {name}.
Respond in JSON output with a 'code' field, filling in the following assertion format:
```
assert ...
assert ...
# Include as many or as few assertions as needed
```
Here is a list of existing unit test assertions and property-based hypothesis tests.
Do not generate any unit tests that are functionally equivalent or whose behavior is already captured by them:
```
{existing}
```"""


def runtime_testing_prompt(tests: str) -> str:
    """Prompt for LLM to generate runtime tests based off of property-based tests list"""

    return f"""Convert each of the following list of property-based Hypothesis tests into an if-condition where the preconditions and the property must both be satisfied.
    If they are true, increment arrays 'property_passes' and 'iteration' by 1 at the index matching the property number. The first property will increment at index 0, the second at index 1, and so on.
    If the preconditions are true but the property fails, increment only the 'iteration' array. If the precondition is not satisfied, do not increment either array.
```
{tests}
```
Respond in JSON output with a 'code' field, using the following format for each Hypothesis test:
```
if (precondition):
    iteration[...] += 1
    if (property):
        property_passes[...] += 1
```"""


def test_case_predicate(obj) -> bool:
    """Returns true if obj is a unittest.TestCase"""

    if inspect.isclass(obj):
        return issubclass(obj, unittest.TestCase)
    return False


def get_test_func_lines_from_testcase(cls) -> list:
    """Gets the source code of all lines given a testcase"""

    ret = []

    funcs = inspect.getmembers(cls, inspect.isfunction)
    for func in funcs:
        if func[1].__module__ != "unittest.case":
            ret.append(inspect.getsourcelines(func[1]))

    return ret


def get_funcs_from_testsuite(suite: unittest.TestSuite) -> list:
    """Gets the source code of all objects within a TestSuite"""

    ret = []

    for test in suite:
        if isinstance(test, unittest.TestSuite):
            ret += get_funcs_from_testsuite(test)

        # is a TestCase
        else:
            ret += get_test_func_lines_from_testcase(test)

    return ret


def prep_unit_tests(tests: list) -> str:
    """Gets the source code of a all unittests in tests and converts it into a string"""

    src = []

    for t in tests:
        if inspect.ismodule(t):
            # do I need the predicate? or can I safely assume a module is all tests
            cases = inspect.getmembers(t, test_case_predicate)
            for cls in cases:
                src += get_test_func_lines_from_testcase(cls[1])
        # there should never be a non-TestCase class here anyways, do I need this?
        elif type(t) == type and issubclass(t, unittest.TestCase):
            src += get_test_func_lines_from_testcase(t)

        elif isinstance(t, unittest.TestSuite):
            src += get_funcs_from_testsuite(t)

    ret = ""

    if src:
        ret += "\nThe function should also pass the following unit tests. Included is their name and source code. Do not write these tests\n\n"

        for func in src:
            for line in func[0]:
                ret += line

            ret += "\n"

    return textwrap.indent(textwrap.dedent(ret), "        ")


def find_aliases_in_import(obj, func) -> str:
    """Finds the name / alias of the module obj is in, in the file of func"""
    # need file path to the original file
    file_path = os.path.abspath(inspect.getfile(func))

    with open(file_path, "r", encoding="utf-8") as file:
        script = file.read()

    tree = ast.parse(script)

    for node in tree.body:
        if isinstance(node, (ast.ImportFrom, ast.Import)):
            for alias in node.names:
                if alias.asname and alias.name in inspect.getmodule(obj).__name__:
                    return alias.asname
                elif alias.name and alias.name in inspect.getmodule(obj).__name__:
                    return alias.name

    return None


def get_mod(obj, func) -> str:
    """Gets module names / aliases of obj and returns it as a string, in the file of func"""
    mod = ""
    prefix = find_aliases_in_import(obj, func)
    if prefix:
        mod = f"{prefix}."

    return mod


def get_bases(obj, func) -> str:
    """Gets the base classes for obj and formats the string, in the file of func"""
    if obj.__bases__:
        bases = ""
        for cls in obj.__bases__:
            # 'object' is a special case that isn't useful
            if cls.__name__ != "object":
                mod = get_mod(obj, func)
                bases += f"({mod}{cls.__qualname__}, "

        bases = bases[:-2]

        # formatting
        if len(bases) > 0:
            bases += ")"

    return bases


def prep_class_or_func(obj, indent: int, func) -> str:
    """Formats the string and docstring for obj, in the file of func"""
    mod = get_mod(obj, func)

    if inspect.isclass(obj):
        bases = get_bases(obj, func)
        str = f"{mod}{obj.__qualname__}{bases}:\n"
    else:
        str = f"{mod}{obj.__qualname__}{inspect.signature(obj)}:\n"

    doc = inspect.getdoc(obj)
    if doc:
        # indent the doc so it's indented relative to the signature / name
        doc = textwrap.indent(f'"""{doc}"""\n...', "    ")
        str = f"{str + doc}\n"

    while indent > 0:
        # indent everything s.t. it is nested within its class
        str = textwrap.indent(str, "    ")
        indent -= 1

    # indent everything so it lines up with the triple-quotation prompt
    return textwrap.indent(f"{str}\n", "            ")


def prep_slots(slots: list) -> str:
    """Converts a list of slots into a string of the format 'class_name: __slots__"""

    str = "\n\nFor each listed class, that class contains only these attributes:\n\n"

    # each slot is a tuple of (name, slots)
    for slot in slots:
        str += f"    {slot[0]}: {slot[1]}\n\n"

    return textwrap.indent(f"{str}\n", "        ")


def convert_list(to_add: list, no_print: list, func, slots: list) -> str:
    """Converts a list of objects to_add into a string for the prompt"""
    str = ""
    indent = 0
    prev_class = ""

    for object in to_add:
        if object.__qualname__ not in no_print:
            if inspect.isclass(object):
                # keep track of previous classes in order to nest things
                preceding_classes = object.__qualname__.rsplit(".", 1)[0]
                if preceding_classes == prev_class:
                    indent += 1
                else:
                    indent = 0

                str += prep_class_or_func(object, indent, func)
                prev_class = object.__qualname__

            # if isfunction:
            else:
                if prev_class == "":
                    str += prep_class_or_func(object, indent, func)
                else:
                    # functions will nest within a class, so increase indent
                    # unless it's global, which is prev_class == ""
                    str += prep_class_or_func(object, indent + 1, func)

    str += prep_slots(slots)

    return str


def get_funcs_from_class(cls: type, target_func) -> list:
    """Returns the list of functions in cls that aren't target_func"""
    ret = []

    funcs = inspect.getmembers(cls, inspect.isfunction)
    for func in funcs:
        # ensure that we don't identify the function we're generating as a usable function
        # compare names because the same function can occupy different places in memory and not be recognized
        if func[1].__qualname__ != target_func.__qualname__:
            ret.append(func[1])

    return ret


def get_complete_class(cls: type, target_func) -> list:
    """Returns a list of every element of cls, including functions and nested classes, except target_func"""
    ret = []

    # grab methods
    ret += get_funcs_from_class(cls, target_func)

    # get nested classes if they exist
    nested_classes = inspect.getmembers(cls, inspect.isclass)
    if nested_classes:
        for nest in nested_classes:
            # a special case that isn't useful
            if nest[0] != "__class__":
                ret.append(nest[1])
                ret += get_funcs_from_class(nest[1], target_func)

    return ret


def prep_entire_file(target_func) -> list:
    """Returns a list of every class and function in target_func's file, except target_func"""
    # module is at the global level
    module = inspect.getmodule(target_func)
    clst = inspect.getmembers(module, inspect.isclass)
    glbl_funcs = inspect.getmembers(module, inspect.isfunction)

    to_add = []
    for func in glbl_funcs:
        to_add.append(func[1])
    for cls in clst:
        to_add.append(cls[1])
        to_add += get_complete_class(cls[1], target_func)

    return to_add


def get_class_from_func(func):
    """Returns func if func is global, returns the innermost class object related to func otherwise"""
    ret = inspect.getmodule(func)
    classes_to_find = func.__qualname__.split(".")[:-1]

    i = 0
    while i < len(classes_to_find):
        class_list = inspect.getmembers(ret, inspect.isclass)

        name = classes_to_find[i]
        for cls in class_list:
            # getmembers returns (name, value)
            if name == cls[0]:
                ret = cls[1]
        i += 1

    if i > 0:
        return ret
    return func


def prep_related_objs(func, related_objs: list, no_print: list) -> str:
    """Prepares the prompt string for related_objs"""

    str = """\
        Below is a list of classes and functions that may be used in the implementation.
        Included is their name, signature, and docstring. Do not declare
        these functions or classes and do not import anything to use them. \n\n"""

    to_add = []
    for obj in related_objs:
        # prep entire file
        if obj == "*":
            to_add += prep_entire_file(func)
        # prep innermost class of func
        elif obj == "cls":
            cls_obj = get_class_from_func(func)
            to_add.append(cls_obj)
            to_add += get_funcs_from_class(cls_obj, func)
        else:
            to_add.append(obj)
            if inspect.isclass(obj):
                to_add += get_funcs_from_class(obj, func)

    slots = []

    for obj in to_add:
        possible_cls = get_class_from_func(obj)
        if type(possible_cls) == type:
            if hasattr(possible_cls, "__slots__"):
                # FIXME: temporary fix, can't use sets since lists are non-hashable
                if (possible_cls.__name__, possible_cls.__slots__) not in slots:
                    slots.append((possible_cls.__name__, possible_cls.__slots__))

    str += convert_list(to_add, no_print, func, slots)

    return str


def prep_tests(tests: list) -> str:
    """Takes a string of tests as input and prepares a string that will be appended to the prompt"""
    final_tests = []

    for t in tests:
        if isinstance(t, tuple):
            final_tests.append(t[1])
        elif isinstance(t, str):
            final_tests.append(t)
        else:
            pass

    if final_tests:
        test_string = "\n".join(final_tests)
        test_string = textwrap.indent(test_string, "    ")
        prompt_string = textwrap.indent(
            f"\nThe function should pass the following tests:\n{test_string}\n",
            "        ",
        )
        return prompt_string
    else:
        return ""


def string_reformat(string: str) -> str:
    """Reformats string so the prompt prints nicely"""
    string_list = string.split("\n")
    ret = ""
    for line in string_list:
        ret += f"\n{textwrap.indent(textwrap.dedent(line), '            ')}"

    return f"{ret}\n"


def prep_signature(func) -> str:
    """Formats the string signature of a func"""
    sig = inspect.signature(func)
    sig_str = str(sig)

    # Use regex to find and remove `__main__.` prefix
    cleaned_sig_str = re.sub(r"__main__\.", "", sig_str)

    return cleaned_sig_str


def prep_imports(func) -> str:
    return textwrap.indent(
        f"""
Below is a list of classes and functions that may be used in the implementation.
Included is their name, signature, and docstring. Do not declare
these functions or classes and do not import anything to use them.
```
{symbols.gather_module_docs(func)}
```
""",
        " " * 8,
    )


def create_prompt(
    function_info: dict,
    spec_string: str,
    tests: list,
    time_bound: str | None,
    mem_bound: str | None,
    func,
    related_objs: list,
    no_print: list,
    generation_reason: str | None = None,
    function_template: str | None = None,
) -> str:
    """Creates a prompt string to send to the LLM"""
    prompt = f"""
        Produce a JSON object with code for a Python function
        named {function_info['function_name']} that performs the following task as
        a field \"code\". Only produce output that can be parsed as
        JSON. \n"""

    if generation_reason:
        prompt += "Be sure to avoid this issue from an earlier version:"
        prompt += string_reformat(generation_reason)
        prompt += "\n"

    # if related_objs:
    #     # handle duplicates
    #     related_objs = list(set(related_objs))
    #     prompt += prep_related_objs(func, related_objs, no_print)

    prompt += prep_imports(func)

    prompt += """
        Task:
        """

    prompt += string_reformat(spec_string)

    prompt += """
        Include a docstring containing the task description above
        (without the word "Task:").  The function should be
        entirely self-contained, with all imports, code, and data, except
        for the above helper functions. Do not define any other functions, classes,
        or methods inside the function you are writing.\n"""

    # if function_template:
    #     prompt += f"""
    #     Fill in the function definition below with your implementation.
    #     Do not change the function name or signature.
    #     ```
    #     {textwrap.indent(function_template, '        ')}
    #     ```
    #     """

    if time_bound:
        prompt += f"""
        The function must have {time_bound} runtime or faster.\n"""

    if mem_bound:
        prompt += f"""
        The function must use {mem_bound} memory or less.\n"""

    if tests:
        prompt += prep_tests(tests)
        prompt += f"{prep_unit_tests(tests)}"

    assert function_template is not None, "Function template not present"
    prompt += f"""
        Return only a single method or function definition. Use this template for your response:
        ```
        {textwrap.indent(function_template, '        ')}
        ```
        """

    return textwrap.dedent(prompt)
