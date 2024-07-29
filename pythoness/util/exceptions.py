class JSONException(Exception):
    """Exception raised when parsing JSON"""
    pass

class CompileException(Exception):
    """Exception raised when compiling"""
    pass

class ExecException(Exception):
    """Exception raised when calling exec()"""
    pass

class TypeCompatibilityException(Exception):
    """Exception raised when type compatability fails"""
    pass

class DefaultMismatchException(Exception):
    """Exception raised when defaults do not match"""
    pass

class TestsException(Exception):
    """Exception raised when tests do not execute"""
    pass

class TestsFailedException(Exception):
    """Exception raised when tests fail"""
    pass
