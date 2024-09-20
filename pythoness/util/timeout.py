class TimeoutException(Exception):
    """Custom exception to handle timeouts"""
    pass

def timeout_handler(signum, frame):
    """Custom handler for timeouts"""
    raise TimeoutException("Function timed out")

