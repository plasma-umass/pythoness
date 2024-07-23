import os
from typing import TypeVar

T = TypeVar('T')

def get_env(option_name: str, default_value: T) -> T:
    """
    Get the value of an environment variable, or return the default value if it is not set.
    """
    env_name = "PYNS_" + option_name.upper()
    v = os.getenv(env_name, str(default_value))
    if isinstance(default_value, bool):
        return v.lower() == "true"
    else:
        return v

class Config:
    """
    Configuration class for NBSketch. This class is used to store the global configuration of the NBSketch system.
    """

    def __init__(self):
        """
        Initialize the configuration class with default values.
        """
        self.verbose_flag = bool(int(get_env("verbose", "0")))
        self.replace_flag = bool(int(get_env("replace", "0")))

config = Config()