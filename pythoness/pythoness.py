from .util import assistant
from .util import database
from .util import timeout
from .util import helper_funcs
from .util import logger
from .util import testing
from .util import prompt_helpers
from .util import config
from contextlib import nullcontext
from functools import wraps
import sys
import signal
import termcolor

# TODO: getting the correct JSON format throws exceptions when not using the correct model -> catch exception in parse JSON?
# TODO: KeyboardInterrupt when hypothesis exiting should exit the whole program using sys.exit()
# TODO: if spec is defined but the function never called, print something out as warning?
 
# TODO: turn related_objs into a set in case of repeats

# TODO: thinking about adding slots

# TODO: What if I do 'cls' in a global function?

# TODO: could I extend testing functionality to accomodate entire functions?

# TODO: might be replacing it in the wrong order

# TODO: test whether adding that line at the beginning of the prompt makes a difference





# Issues to fix:
# check if subclasses work
# What if I do 'cls' in a global function?
# perhaps change the __qualname__ to __name__ if it falls under the target class? (but it doesn't seem to be decreasing consistency)

# Things to add (goal: increase consistency):
# Expected -> actual for testing
# Generating more test cases automatically so it will check itself 
# test subclasses
# possibly get __slots__ to increase consistency?
# 'self' option for possible functions

# IDEA: get expected and actual out of tests



globals_no_print = []
cdb = database.CodeDatabase('pythoness-cache.db')
cost = 0

def spec(string, model="gpt-4o", replace=None, tests=None, max_retries=3, verbose=None, output=False, regenerate=False, related_objs=None, timeout_seconds=0):
    ''' Main logic of Pythoness '''

    if verbose is None:
        verbose = config.config.verbose_flag
    
    if replace is None:
        replace = config.config.replace_flag

    def decorator(func):
        cached_function = None
        
        log = logger.Logger()
        
        if func.__doc__:
            func.__doc__ += string
        else:
            func.__doc__ = string

        @wraps(func)
        def wrapper(*args, **kwargs):
            # log("Start") in the wrapper so something must be wrapped
            # in order for "Start" to appear
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

                with log("[Pythoness] Getting function info...") if verbose else nullcontext():
                    # function_info = helper_funcs.get_function_info(func, *args, **kwargs)
                    function_info = helper_funcs.get_function_info(func)

                with log("[Pythoness] Creating prompt and checking the DB...") if verbose else nullcontext():
                    prompt = prompt_helpers.create_prompt(function_info, string, tests, func, related_objs, globals_no_print)
                    function_info = helper_funcs.setup_info(function_info, func, string, prompt)

                # See if we already have code corresponding with that prompt in the database.
                    if regenerate:
                        # Force regeneration by ignoring any existing code in the database
                        function_def = None
                    else: 
                        function_def = cdb.get_code(prompt)

                    if verbose and not function_def:
                        log.log('[Pythoness] Prompt:\n', prompt)

                # We have previously loaded the function. Just execute it and return.
                    if function_def:
                        if verbose:
                            log.log("[Pythoness] Retrieved function from database:\n", function_def)
                        
                        if replace: 
                            
                            with log("[Pythoness] Replacing...") if verbose else nullcontext(): 
                                helper_funcs.replace_func(func, function_def)

                        globals_no_print.append(function_info['function_name'])
                        return helper_funcs.database_compile(function_info, function_def, *args, **kwargs)

                
                with log("[Pythoness] Generating code...") if verbose else nullcontext():
                
                    while function_info['retries'] < max_retries:
                        signal.signal(signal.SIGALRM, timeout.timeout_handler)
                        signal.alarm(timeout_seconds)

                        try:
                            function_info['retries'] += 1

                            if verbose:
                                log.log(f'[Pythoness] Attempt {function_info['retries']}')

                            with log("[Pythoness] Parsing...") if verbose else nullcontext():
                                function_info = helper_funcs.parse_func(function_info, client, prompt, verbose, log)

                            # store code in databse so the tests can run it
                            cdb.insert_code(function_info["original_prompt"], function_info['function_def'])

                            with log("[Pythoness] Compiling...") if verbose else nullcontext():
                                function_info = helper_funcs.compile_func(function_info)

                            with log("[Pythoness] Executing...") if verbose else nullcontext():
                                function_info = helper_funcs.execute_func(function_info)
                            
                            fn = function_info['globals'][function_info['function_name']]                            
                            
                            with log("[Pythoness] Validating types...") if verbose else nullcontext():
                                testing.validate_types(func, fn)

                            if tests:
                                with log("[Pythoness] Validating tests...") if verbose else nullcontext():
                                    testing.validate_tests(function_info, tests, log)
                                    
                            # Validated. Cache the function and persist it
                            cached_function = fn
                            cdb.insert_code(function_info['original_prompt'], function_info['function_def'])
                            if output:
                                print(termcolor.colored(f"\n[Pythoness] Output:\n{function_info['function_def']}\n", "green"), file=sys.stdout)

                            if replace: 
                                
                                with log("[Pythoness] Replacing...") if verbose else nullcontext():   
                                        helper_funcs.replace_func(func, function_info['function_def'])
                                
                            globals_no_print.append(function_info['function_name'])  
                            
                            return cached_function(*args, **kwargs)
                        
                        except Exception as e:
                            func.__globals__.pop(function_info['function_name'])
                            # code is stored in database so tests can run it, need to make sure it's cleared
                            cdb.delete_code(function_info["original_prompt"])
                            prompt = helper_funcs.exception_handler(e, verbose, log)
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
                                global cost
                                cost += client.get_stats('cost')
                                log.log(f"\n[Total cost so far: ~${cost:.2f} USD]")

                # If we got here, we had too many retries.
                # ensure that nothing is in the DB to interfere with a future call
                cdb.delete_code(function_info["original_prompt"])
                raise Exception(f'Maximum number of retries exceeded ({max_retries}).')
        return wrapper
    return decorator

