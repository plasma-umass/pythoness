import sys
import types
import inspect
import ast

# List of allowed special methods.
ALLOWED_SPECIAL = {"__init__", "__call__", "__str__", "__repr__"}


def format_signature(obj):
    """
    Return the signature string for callable objects.
    For non-callable objects, simply return an empty string.
    Uses inspect for objects available at runtime.
    """
    if callable(obj):
        try:
            if inspect.isclass(obj) and hasattr(obj, "__init__"):
                sig = inspect.signature(obj.__init__)
                params = list(sig.parameters.values())
                if params and params[0].name == "self":
                    params = params[1:]
                return f"({', '.join(str(p) for p in params)})"
            else:
                sig = inspect.signature(obj)
                return str(sig)
        except Exception:
            return ""
    return ""


def ast_signature(func_node):
    """
    Build a signature string from an AST FunctionDef node.
    This is a simplified version that lists the parameter names.
    """
    params = []
    for arg in func_node.args.args:
        params.append(arg.arg)
    if func_node.args.vararg:
        params.append("*" + func_node.args.vararg.arg)
    for arg in func_node.args.kwonlyargs:
        params.append(arg.arg)
    if func_node.args.kwarg:
        params.append("**" + func_node.args.kwarg.arg)
    return f"({', '.join(params)})"


def get_base_classes(node):
    """
    Given an ast.ClassDef node, return a string listing its base classes.
    Uses ast.unparse if available (Python 3.9+), otherwise a simple fallback.
    """
    bases = []
    for base in node.bases:
        try:
            if hasattr(ast, "unparse"):
                base_str = ast.unparse(base)
            else:
                if isinstance(base, ast.Name):
                    base_str = base.id
                elif isinstance(base, ast.Attribute):
                    base_str = (
                        f"{base.value.id}.{base.attr}"
                        if isinstance(base.value, ast.Name)
                        else base.attr
                    )
                else:
                    base_str = str(base)
            bases.append(base_str)
        except Exception:
            bases.append("<unknown>")
    return ", ".join(bases) if bases else ""


def format_symbol_ast(node, exclude_method=None):
    """
    Given an AST node for a FunctionDef or ClassDef, return a formatted string
    resembling pydoc output.

    For functions, if a decorator named pythoness.spec is present,
    extract its first argument (the spec string) and use that instead of the docstring.

    For classes, include base classes, the __init__ signature, __slots__ (if any),
    and then the members (methods) indented further. When listing members,
    exclude names that start and end with double underscores except for allowed specials.
    Also, if exclude_method is provided as a tuple (target_class, target_method),
    and the current class name matches target_class, skip the member with that method name.
    """
    result_lines = []
    if isinstance(node, ast.FunctionDef):
        signature = ast_signature(node)
        header = f"def {node.name}{signature}:"
        spec_doc = None
        for dec in node.decorator_list:
            if isinstance(dec, ast.Call):
                if (
                    isinstance(dec.func, ast.Attribute)
                    and isinstance(dec.func.value, ast.Name)
                    and dec.func.value.id == "pythoness"
                    and dec.func.attr == "spec"
                ):
                    if dec.args:
                        try:
                            spec_doc = ast.literal_eval(dec.args[0])
                        except Exception:
                            spec_doc = None
                    break
        if spec_doc is not None:
            doc = spec_doc
        else:
            doc = ast.get_docstring(node) or "No documentation available."
        doc_lines = doc.splitlines()
        indented_doc = "\n    ".join(doc_lines)
        result_lines.append(f"{header}\n    {indented_doc}")
    elif isinstance(node, ast.ClassDef):
        init_signature = "()"
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                init_signature = ast_signature(item)
                if init_signature.startswith("(") and init_signature.endswith(")"):
                    params = [p.strip() for p in init_signature[1:-1].split(",")]
                    if params and params[0] == "self":
                        params = params[1:]
                    init_signature = f"({', '.join(params)})"
                break
        header = f"class {node.name}{init_signature}:"
        result_lines.append(header)
        bases_str = get_base_classes(node)
        if bases_str:
            result_lines.append(f"    Bases: {bases_str}")
        doc = ast.get_docstring(node) or "No documentation available."
        doc_lines = doc.splitlines()
        result_lines.append("    " + "\n    ".join(doc_lines))
        slots = None
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id == "__slots__":
                        try:
                            slots = ast.literal_eval(item.value)
                        except Exception:
                            slots = "Could not evaluate __slots__"
                        break
            if slots is not None:
                break
        if slots is not None:
            result_lines.append(f"    Slots: {slots!r}")
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                # Exclude dunder methods unless allowed.
                if (
                    item.name.startswith("__")
                    and item.name.endswith("__")
                    and item.name not in ALLOWED_SPECIAL
                ):
                    continue
                # If we have exclude_method info and the current class matches, skip the method.
                if (
                    exclude_method is not None
                    and node.name == exclude_method[0]
                    and item.name == exclude_method[1]
                ):
                    continue
                member_doc = format_symbol_ast(item, exclude_method=exclude_method)
                indented_member = "\n".join(
                    "    " + line for line in member_doc.splitlines()
                )
                result_lines.append(indented_member)
    else:
        header = f"{node.__class__.__name__} {getattr(node, 'name', '')}:"
        result_lines.append(header)
    return "\n".join(result_lines)


def format_symbol_with_indent(name, obj, indent=0):
    """
    Format a runtime symbol (from __globals__ or class __dict__) similar to pydoc,
    with each line indented by the given number of spaces.
    """
    base = format_symbol(name, obj)
    spaces = " " * indent
    return "\n".join(spaces + line for line in base.splitlines())


def format_runtime_class(name, cls, indent=0):
    """
    Format an imported class similar to pydoc output:
      - Include its header (name, signature, docstring)
      - List its __slots__ if defined
      - List its members from its __dict__, using the same formatting.
        Exclude members with names both prefixed and suffixed by '__'
        unless they are in the allowed list.
    """
    lines = []
    signature = format_signature(cls)
    header = f"class {name}{signature}:"
    lines.append(header)
    doc = inspect.getdoc(cls) or "No documentation available."
    doc_lines = doc.splitlines()
    lines.append("    " + "\n    ".join(doc_lines))
    slots = getattr(cls, "__slots__", None)
    if slots is not None:
        lines.append(f"    Slots: {slots!r}")
    members = cls.__dict__
    for mem_name in sorted(members):
        if (
            mem_name.startswith("__")
            and mem_name.endswith("__")
            and mem_name not in ALLOWED_SPECIAL
        ):
            continue
        mem_obj = members[mem_name]
        member_str = format_symbol_with_indent(mem_name, mem_obj, indent=4)
        lines.append(member_str)
    if indent:
        prefix = " " * indent
        return "\n".join(prefix + line for line in lines)
    return "\n".join(lines)


def format_symbol(name, obj):
    """
    Format a runtime symbol (from __globals__) similar to pydoc.
    For classes and functions, show a header and an indented docstring.
    """
    signature = format_signature(obj)
    doc = inspect.getdoc(obj) or "No documentation available."
    if inspect.isclass(obj):
        header = f"class {name}{signature}:"
    elif inspect.isfunction(obj):
        header = f"def {name}{signature}:"
    else:
        header = f"{name}{signature}:"
    doc_lines = doc.splitlines()
    indented_doc = "\n    ".join(doc_lines)
    return f"{header}\n    {indented_doc}"


def gather_module_docs(func):
    output_lines = []

    # Determine if target is a method.
    target_info = None
    if hasattr(func, "__qualname__") and "." in func.__qualname__:
        # For example, "ClassName.methodname"
        parts = func.__qualname__.split(".")
        if len(parts) >= 2:
            target_info = (parts[-2], parts[-1])

    # --- Gather documentation for imported (non-system) modules ---
    module_sections = []
    for name, obj in func.__globals__.items():
        if isinstance(obj, types.ModuleType):
            if not hasattr(obj, "__file__"):
                continue
            if obj.__file__.startswith(sys.prefix):
                continue
            if "pythoness" in obj.__name__:
                continue

            mod_doc = inspect.getdoc(obj) or "No module documentation available."
            mod_header = (
                f"MODULE {obj.__name__}\n{'-' * (7 + len(obj.__name__))}\n{mod_doc}"
            )
            module_lines = [mod_header]
            for symbol in sorted(dir(obj)):
                try:
                    attr = getattr(obj, symbol)
                except Exception:
                    continue
                if inspect.isclass(attr):
                    class_str = format_runtime_class(symbol, attr, indent=4)
                    module_lines.append(class_str)
                else:
                    module_lines.append(
                        format_symbol_with_indent(symbol, attr, indent=4)
                    )
            module_sections.append("\n".join(module_lines))

    if module_sections:
        output_lines.append("Imported Modules:")
        output_lines.append("\n\n".join(module_sections))

    # --- Gather documentation for symbols defined in the current file using AST ---
    local_symbols = []
    filename = inspect.getsourcefile(func)
    try:
        with open(filename, "r") as f:
            source = f.read()
    except Exception as e:
        source = ""
        local_symbols.append(f"Error reading source file: {e}")

    if source:
        mod_ast = ast.parse(source, filename)
        for node in mod_ast.body:
            # If the target is not a method, skip top-level function matching target name.
            if target_info is None:
                if isinstance(node, ast.FunctionDef) and node.name == func.__name__:
                    continue
            # For classes and functions, process them.
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                local_symbols.append(
                    format_symbol_ast(node, exclude_method=target_info)
                )

    if local_symbols:
        output_lines.append("Local Symbols:")
        output_lines.append("\n".join(local_symbols))

    return "\n\n".join(output_lines)


# --- Example usage ---


def sample_function(a, b):
    """Return the sum of a and b."""
    return a + b


# Example decorator for demonstration purposes.
def dummy_decorator(arg):
    def wrapper(func):
        return func

    return wrapper


# Mimic the pythoness.spec decorator.
class pythoness:
    @staticmethod
    def spec(spec_string):
        def decorator(func):
            return func

        return decorator


@pythoness.spec(
    "This is the SPEC for decorated_function: it takes two numbers and returns their product."
)
def decorated_function(x, y):
    return x * y


class SampleClass:
    """A sample class to demonstrate local symbols with __slots__."""

    __slots__ = ("x", "y")

    def __init__(self, x):
        """Initialize with x."""
        self.x = x

    def method(self, y):
        """Return the sum of x and y."""
        return self.x + y

    def extra_method(self, z):
        """An extra method that multiplies x by z."""
        return self.x * z

    def __hidden_method(self):
        """This should be excluded."""
        pass


def function_to_process(x, y):
    """Function whose scope will be inspected via AST for local symbols.
    (This function is not included in the output as a top-level function.)
    If it is a method, then only its entry is skipped from its class."""
    result = sample_function(x, y)
    obj = SampleClass(result)
    prod = decorated_function(x, y)
    return obj.method(x)


if __name__ == "__main__":
    output = gather_module_docs(function_to_process)
    print(output)
