import inspect
import textwrap

# NOTE: formatting looks good in verbose, but it's terrible in code

def prep_class_or_func(obj, indent):
    ""
    if inspect.isclass(obj):
        str = f"{obj.__qualname__}:\n"
    else:
        str = f"{obj.__qualname__}{inspect.signature(obj)}:\n"

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

def convert_list(to_add):
    str = ""
    indent = 0
    prev_class = ""

    for object in to_add:
        if inspect.isclass(object):

            # keep track of previous classes in order to nested things
            # appropriately
            preceding_classes = object.__qualname__.rsplit('.', 1)[0]
            if preceding_classes == prev_class:
                indent += 1
            else:
                indent = 0
                    
            str += prep_class_or_func(object, indent)
            prev_class = object.__qualname__

        # isfunction
        else:
            if prev_class == "":
                str += prep_class_or_func(object, indent)
            else:
                # functions will nest within a class
                # unless it's global, which is prev_class == ""
                str += prep_class_or_func(object, indent + 1)

    return str


def get_funcs_from_class(cls, target_func):
    ret = []

    funcs = inspect.getmembers(cls, inspect.isfunction)
    for func in funcs:
        # ensure that we don't identify the function we're generating as a usable function
        # compare names because the same function can occupy different places in memory and not be recognized
        if func[0] != target_func.__name__:
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
    
    str = convert_list(to_add) 

    return str

def prep_related_objs(func, related_objs):

    str = """\
        Below is a list of functions that may be used in the implementation.
        Included is their name, signature, and docstring. Do not write
        these functions. \n\n""" 

    if related_objs == '*':
       str += prep_entire_file(func)

    else:
        to_add = []
        for obj in related_objs:
            to_add.append(obj)
            if inspect.isclass(obj):
                to_add += get_funcs_from_class(obj, func)

        str += convert_list(to_add)

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
        

def create_prompt(function_info, string, tests, func, related_objs):
    ''' Creates a prompt string to send to the LLM '''
    prompt = f"""
        Produce a JSON object with code for a Python function
        named {function_info['function_name']} that performs the following task as
        a field \"code\". Only produce output that can be parsed as
        JSON. \n\n"""
    if related_objs:
        prompt += prep_related_objs(func, related_objs)

    prompt +="""\
        Task:
        """
    
    prompt += string_reformat(string)

    prompt += """
        Include a docstring containing the task description above
        (without the word "Task:").  The function should be
        entirely self-contained, with all imports, code, and data, except
        for the above helper functions. Do not include any tests 
        in the function.\n"""
    
    if tests:
        prompt += prep_tests(tests)

    prompt += f"""
        The function should have the following signature:
            {inspect.signature(func)}
        """
    
    return textwrap.dedent(prompt)

