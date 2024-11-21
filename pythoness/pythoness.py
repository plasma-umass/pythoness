from .util import assistant
from .util import database
from .util import timeout
from .util import helper_funcs
from .util import logger
from .util import testing
from .util import prompt_helpers
from .util import config
from .util import execution_testing
from contextlib import nullcontext
from functools import wraps
import sys
import signal
import termcolor

# exec() pushes function to the global scope
# globals_no_print ensures they aren't included twice in the prompt
globals_no_print = []
cdb = database.CodeDatabase("pythoness-cache.db")
cost = 0
time = 0


def spec(
    string,
    model="gpt-4o",
    exec=None,
    replace=None,
    tests=None,
    test_descriptions=None,
    max_retries=3,
    verbose=None,
    output=False,
    regenerate=False,
    related_objs=None,
    timeout_seconds=0,
):
    """Main logic of Pythoness"""

    if verbose is None:
        verbose = config.config.verbose_flag

    if replace is None:
        replace = config.config.replace_flag

    def decorator(func):
        cached_function = None

        log = logger.Logger(quiet=config.config.quiet_flag)

        # enables interrelated function generation
        if func.__doc__:
            func.__doc__ += string
        else:
            func.__doc__ = string

        @wraps(func)
        def wrapper(*args, **kwargs):
            with log("Start") if verbose else nullcontext():

                nonlocal cached_function
                if regenerate:
                    # Clear the cached function if we are regenerating.

                    cached_function = None

                # If we've already built this function and cached it, just
                # run it

                if cached_function:
                    return cached_function(*args, **kwargs)

                client = assistant.Assistant(model=model)

                # We need to generate a function from the spec.
                # We populate the prompt with the function's name, argument name and types, and the return type.

                with (
                    log("[Pythoness] Getting function info...")
                    if verbose
                    else nullcontext()
                ):
                    # function_info = helper_funcs.get_function_info(func, *args, **kwargs)
                    function_info = helper_funcs.get_function_info(func)

                with (
                    log("[Pythoness] Creating prompt and checking the DB...")
                    if verbose
                    else nullcontext()
                ):
                    prompt = prompt_helpers.create_prompt(
                        function_info,
                        string,
                        tests,
                        func,
                        related_objs,
                        globals_no_print,
                    )
                    function_info = helper_funcs.setup_info(
                        function_info, func, string, prompt
                    )

                    # See if we already have code corresponding with that prompt in the database.
                    if regenerate:
                        # Force regeneration by ignoring any existing code in the database
                        function_def = None
                    else:
                        function_def = cdb.get_code(prompt)

                    if verbose and not function_def:
                        log.log("[Pythoness] Prompt:\n", prompt)

                    # We have previously loaded the function. Just execute it and return.
                    if function_def:
                        if verbose:
                            log.log(
                                "[Pythoness] Retrieved function from database:\n",
                                function_def,
                            )

                        if replace:

                            with (
                                log("[Pythoness] Replacing...")
                                if verbose
                                else nullcontext()
                            ):
                                helper_funcs.replace_func(func, function_def)

                        globals_no_print.append(function_info["function_name"])
                        return helper_funcs.database_compile(
                            function_info, function_def, *args, **kwargs
                        )

                with (
                    log("[Pythoness] Generating code...") if verbose else nullcontext()
                ):

                    while function_info["retries"] < max_retries:
                        signal.signal(signal.SIGALRM, timeout.timeout_handler)
                        signal.alarm(timeout_seconds)

                        try:
                            function_info["retries"] += 1

                            if verbose:
                                log.log(
                                    f'[Pythoness] Attempt {function_info["retries"]}'
                                )

                            with (
                                log("[Pythoness] Parsing...")
                                if verbose
                                else nullcontext()
                            ):
                                function_info = helper_funcs.parse_func(
                                    function_info,
                                    client,
                                    prompt,
                                    verbose,
                                    log,
                                )

                            # store code in database so the tests can run it
                            cdb.insert_code(
                                function_info["original_prompt"],
                                function_info["function_def"],
                            )

                            with (
                                log("[Pythoness] Compiling...")
                                if verbose
                                else nullcontext()
                            ):
                                function_info = helper_funcs.compile_func(function_info)

                            with (
                                log("[Pythoness] Executing...")
                                if verbose
                                else nullcontext()
                            ):
                                function_info = helper_funcs.execute_func(function_info)

                            fn = function_info["globals"][
                                function_info["function_name"]
                            ]

                            with (
                                log("[Pythoness] Validating types...")
                                if verbose
                                else nullcontext()
                            ):
                                testing.validate_types(func, fn, function_info)

                            tests_to_run = None
                            if tests or test_descriptions:
                                with (
                                    log("[Pythoness] Generating tests...")
                                    if verbose
                                    else nullcontext()
                                ):
                                    tests_to_run, property_tests = (
                                        testing.generate_tests(
                                            function_info,
                                            tests,
                                            test_descriptions,
                                            client,
                                            log,
                                            verbose,
                                        )
                                    )

                            if tests_to_run:
                                with (
                                    log("[Pythoness] Validating tests...")
                                    if verbose
                                    else nullcontext()
                                ):
                                    testing.validate_tests(
                                        function_info,
                                        tests_to_run,
                                        log,
                                    )

                            # Validated. Cache the function and persist it
                            if exec is None:
                                cached_function = fn
                            else:
                                if verbose:
                                    log.log(
                                        "[Pythoness] Adding execution-time testing framework..."
                                    )
                                function_info = execution_testing.add_execution_testing(
                                    function_info, property_tests, cdb
                                )
                                cached_function = function_info["globals"][
                                    function_info["function_name"]
                                ]

                            if output:
                                print(
                                    termcolor.colored(
                                        f"\n[Pythoness] Output:\n{function_info['function_def']}\n",
                                        "green",
                                    ),
                                    file=sys.stdout,
                                )

                            if replace:
                                with (
                                    log("[Pythoness] Replacing...")
                                    if verbose
                                    else nullcontext()
                                ):
                                    helper_funcs.replace_func(
                                        func, function_info["function_def"]
                                    )

                            globals_no_print.append(function_info["function_name"])

                            return cached_function(*args, **kwargs)

                        except Exception as e:
                            try:
                                func.__globals__.pop(function_info["function_name"])
                            except:
                                pass
                            # code is stored in database so tests can run it, need to make sure it's cleared
                            cdb.delete_code(function_info["original_prompt"])
                            prompt = helper_funcs.exception_handler(
                                e, verbose, log, func, related_objs, globals_no_print
                            )
                            continue

                        # ensures regeneration on future attempts
                        # KeyboardIntterupts are not caught by general exceptions
                        except KeyboardInterrupt:
                            cdb.delete_code(function_info["original_prompt"])
                            sys.exit()

                        except SystemExit:
                            cdb.delete_code(function_info["original_prompt"])
                            sys.exit()

                        finally:
                            signal.alarm(0)
                            if verbose:
                                global cost, time
                                cost += client.get_stats("cost")
                                time += client.get_stats("time")
                                log.log(f"\n[Total cost so far: ~${cost:.2f} USD]")
                                log.log(f"\n[Total time so far: {time}]")

                # If we got here, we had too many retries.
                # ensure that nothing is in the DB to interfere with a future call
                cdb.delete_code(function_info["original_prompt"])
                raise Exception(f"Maximum number of retries exceeded ({max_retries}).")

        return wrapper

    return decorator
