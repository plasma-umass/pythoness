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
from bigO import check

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

    length_func = None,
    time_bound = None,
    # mem_bound = None;
    generate_func = None,

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

        # if time_bound:
        #     func = bigO.check(length_func, time_bound = time_bound)(func)

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
                        time_bound,
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
                        fn = helper_funcs.database_compile(
                            function_info, function_def, length_func, time_bound
                        )

                        return fn(*args, **kwargs)

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
                                if function_info["retries"] > 0:
                                    log.log(f"[Pythoness] New prompt:\n\n{prompt}\n")

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

                            # if time_bound:
                            #     function_info["globals"][function_info["function_name"]] = check(length_func, time_bound = time_bound)(function_info["globals"][function_info["function_name"]])

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

                            if time_bound:
                                with(
                                    log("[Pythoness] Validating time bound...")
                                    if verbose
                                    else nullcontext()
                                ):
                                    
                                    # interpreter gets weird when I reassign generate_func
                                    if isinstance(generate_func, str):
                                        generator = testing.generate_generator_func(
                                            generate_func,
                                            fn,
                                            function_info,
                                            model,
                                            log,
                                            verbose
                                        )
                                    else:
                                        generator = generate_func

                                    testing.validate_runtime(
                                        function_info,
                                        generator,
                                        length_func,
                                        time_bound,
                                        log,
                                        verbose
                                    )

                            # Validated. Cache the function and persist it
                            # if exec is None:
                            if True:  # Change to above line to enable execution testing
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

                            # TODO: this won't have the check() wrapper
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




# try to trigger a pythoness rerun when there is an error
# try to get the llm to generate stuff
     # chatgpt gice me a fucntion that generates arrays of size 1 to 1 million

     #TODO:
     # figure out pythoness rereuns on error
     # get some examples going

# TODO: 1/13

# make the programmer include a generator
# so write a function that has a formatted prompt
# ^ this is supposed to say write an LLM generator -> done (kinda finicky, need to test)

# the bigger the bound is, the more likely the dominate cost will reveal itself
# rather than picking random inputs, start with the biggest ones and move down to the smaller ones
# or perhaps generate a bunch and take only a handful of the biggest ones
# stash a version of code that is tricked with the wrong bounds and see what we can do to guide it to the correct bounds

# or perhaps, sample uniformly

# grab the code and stick it somewhere when something is interesting; this gives a good environment to more effectively explore bigO

# I can perhaps lower frequency

# is there a way we can assess the quality of the test case?

# gather some plots and save them
    # plots only generate on exception -> solved

# read that Katie paper

# keep in mind: how we generate inputs impacts how we can interpret the results

# for the writing at the end of the month: what sub-goal are we trying to accomplish with each component of our system?




