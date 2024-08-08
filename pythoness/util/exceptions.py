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
    def __init__(self, normal_tests_failed, unittests_failed):
        self.normal_tests_failed = normal_tests_failed
        self.unittests_failed = unittests_failed

class MaxRetriesException(Exception):
    pass