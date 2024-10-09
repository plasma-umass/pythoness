from . import exceptions
import unittest
import os


class CustomTestResult(unittest.TextTestResult):
    def addError(self, test, err):
        super().addError(test, err)
        if isinstance(err[0], exceptions.MaxRetriesException):
            os._exit(1)
        if isinstance(err[0], KeyboardInterrupt):
            os._exit(1)


class CustomTextTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTestResult(self.stream, self.descriptions, self.verbosity)
