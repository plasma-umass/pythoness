from contextlib import nullcontext
from functools import wraps
import random
import threading
from typing import Any, Callable, Dict

import pythoness
from . import logger
from bigO import bigO

thread_local = threading.local()
thread_local.in_call = False

# func should already be tracked
def check_and_call(
    pythoness_args: Dict[str, Any],
    function_info: dict,
    log: logger.Logger,
    verbose: bool,
    check_frequency=5,
) -> Callable:

    length_function = pythoness_args["length_func"]
    time = pythoness_args["time_bound"]
    mem = pythoness_args["mem_bound"]

    def decorator(func: Callable) -> Callable:

        tracked = bigO.bounds(length_function, time=time, mem=mem)(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if thread_local.in_call:
                    return func(*args, **kwargs)
                thread_local.in_call = True
                log("Checking runtime bounds")
                if random.random() < 1 / check_frequency:
                    with log("Checking runtime bounds") if verbose else nullcontext():
                        try:
                            results = bigO.check(tracked)
                            for result in results:
                                if not result.success:
                                    with (
                                        log("Runtime bounds check failed")
                                        if verbose
                                        else nullcontext()
                                    ):
                                        return pythoness.spec(
                                            **(
                                                pythoness_args
                                                | {
                                                    "generation_reason": result.message,
                                                    "regenerate": True,
                                                }
                                            )
                                        )(func)(*args, **kwargs)
                        except Exception as e:
                            log(f"Exception during runtime bounds check: {e}")
                else:
                    if verbose:
                        log("Skipping runtime bounds check")

                return tracked(*args, **kwargs)
            finally:
                thread_local.in_call = False

        return wrapper

    return decorator


def add_runtime_bounds_testing(
    function_info: dict,
    pythoness_args: Dict[str, Any],
    fn,
    log: logger.Logger,
    verbose: bool,
    cdb,
) -> dict:

    fn = check_and_call(pythoness_args, function_info, log, verbose)(fn)

    function_info["compiled"] = fn

    # Remove and replace the code being stored in the database
    cdb.delete_code(
        function_info["original_prompt"],
    )
    cdb.insert_code(
        function_info["original_prompt"],
        function_info["function_def"],
    )
    return function_info
