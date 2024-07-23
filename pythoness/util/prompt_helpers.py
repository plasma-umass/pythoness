import inspect
import textwrap
import re
import ast
import os

def find_aliases_in_import(obj, func):
    ""
    # need file path to the original file
    file_path = os.path.abspath(inspect.getfile(func))

    with open(file_path, 'r', encoding='utf-8') as file:
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

def get_mod(obj, func):
    mod = ""
    prefix = find_aliases_in_import(obj, func)
    if prefix:
        mod = f"{prefix}."

    return mod

def get_bases(obj, func):
    if obj.__bases__:
        bases = ""
        for cls in obj.__bases__:
            if cls.__name__ != 'object':
                mod = get_mod(obj, func)
                bases += f'({mod}{cls.__qualname__}, '

        bases = bases[:-2]

        if len(bases) > 0:
            bases += ')'

    return bases

def prep_class_or_func(obj, indent, func):
    # need to ensure that I only grab the necessary parts of the module, see blackjack for an example 
    # use rsplit and grab all but the last element in the list
    ""
    mod = get_mod(obj, func)

    if inspect.isclass(obj):
        bases = get_bases(obj, func)
        str = f"{mod}{obj.__qualname__}{bases}:\n"
    else:
        str = f"{mod}{obj.__qualname__}{inspect.signature(obj)}:\n"

    doc = inspect.getdoc(obj)
    if doc:
        # indent the doc so it's indented relative to the signature / name
        doc = textwrap.indent(f"\"\"\"{doc}\"\"\"\n...", "    ")
        str = f"{str + doc}\n"

    while indent > 0:
        # indent everything s.t. it is nested within its class
        str = textwrap.indent(str, "    ")
        indent -= 1
    
    # indent everything so it lines up with the triple-quotation prompt
    return textwrap.indent(f"{str}\n", "            ")

def convert_list(to_add, no_print, func):
    str = ""
    indent = 0
    prev_class = ""

    for object in to_add:
        if object.__qualname__ not in no_print:
            if inspect.isclass(object):

                # keep track of previous classes in order to nested things
                # appropriately
                preceding_classes = object.__qualname__.rsplit('.', 1)[0]
                if preceding_classes == prev_class:
                    indent += 1
                else:
                    indent = 0

                str += prep_class_or_func(object, indent, func)
                prev_class = object.__qualname__

            # isfunction
            else:
                if prev_class == "":
                    str += prep_class_or_func(object, indent, func)
                else:
                    # functions will nest within a class
                    # unless it's global, which is prev_class == ""
                    str += prep_class_or_func(object, indent + 1, func)

    return str


def get_funcs_from_class(cls, target_func):
    ret = []

    funcs = inspect.getmembers(cls, inspect.isfunction)
    for func in funcs:
        # ensure that we don't identify the function we're generating as a usable function
        # compare names because the same function can occupy different places in memory and not be recognized
        if func[1].__qualname__ != target_func.__qualname__:
            ret.append(func[1])
    
    return ret

def get_complete_class(cls, target_func):
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

def prep_entire_file(target_func):
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
    ret = inspect.getmodule(func)
    classes_to_find = func.__qualname__.split('.')[:-1]

    i = 0
    while (i < len(classes_to_find)):
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

def prep_related_objs(func, related_objs, no_print):

    str = """\
        Below is a list of functions that may be used in the implementation.
        Included is their name, signature, and docstring. Do not write
        these functions and do not import anything to use them. \n\n""" 

    if related_objs == '*':
       to_add = prep_entire_file(func)

    else:
        to_add = []
        for obj in related_objs:
            if obj == "cls":
                cls_obj = get_class_from_func(func)
                to_add.append(cls_obj)
                to_add += get_funcs_from_class(cls_obj, func)
            else:
                to_add.append(obj)
                if inspect.isclass(obj):
                    to_add += get_funcs_from_class(obj, func)
    
    

    str += convert_list(to_add, no_print, func)

    return str 

def prep_tests(tests):
    ''' Takes a string of tests as input and prepares a string that will be appended to the prompt '''
    final_tests = []
    for t in tests:
        if isinstance(t, tuple):
            final_tests.append(t[1])
        elif isinstance(t, str):
            final_tests.append(t)
        else:
            pass
    test_string = '\n'.join(final_tests)
    test_string = textwrap.indent(test_string, "    ")
    prompt_string = textwrap.indent(f"\nThe function should pass the following tests:\n{test_string}\n", "        ")
    return prompt_string


def string_reformat(string):
    string_list = string.split('\n')
    ret = ""
    for line in string_list:
        ret += f"\n{textwrap.indent(textwrap.dedent(line), "            ")}"

    return f"{ret}\n"
        

def prep_signature(func):
    sig = inspect.signature(func)
    sig_str = str(sig)

    # Use regex to find and remove `__main__.` prefix
    cleaned_sig_str = re.sub(r'__main__\.', '', sig_str)

    return cleaned_sig_str



def create_prompt(function_info, string, tests, func, related_objs, no_print):
    ''' Creates a prompt string to send to the LLM '''
    prompt = f"""
        Produce a JSON object with code for a Python function
        named {function_info['function_name']} that performs the following task as
        a field \"code\". Only produce output that can be parsed as
        JSON. \n\n"""
    
    if related_objs:
        # handle duplicates
        related_objs = list(set(related_objs))
        prompt += prep_related_objs(func, related_objs, no_print)

    prompt +="""\
        Task:
        """
    
    prompt += string_reformat(string)

    prompt += """
        Include a docstring containing the task description above
        (without the word "Task:").  The function should be
        entirely self-contained, with all imports, code, and data, except
        for the above helper functions. Do not include any tests 
        in the function, and do not write any other functions, classes,
        or methods.\n"""
    
    if tests:
        prompt += prep_tests(tests)

    prompt += f"""
        Return only a method or function definition. Use this template for your response:
            def {function_info['function_name']}{prep_signature(func)}:
                ...
        """
    
    return textwrap.dedent(prompt)

