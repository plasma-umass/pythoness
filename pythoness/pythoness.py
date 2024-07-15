from .util import assistant
from .util import database
from .util import timeout
from .util import helper_funcs
from .util import logger
from .util import testing
from .util import prompt_helpers
from contextlib import nullcontext
from functools import wraps
import sys
import signal
import termcolor

# TODO: grab docstrings so it can automatically use function defs and stuff

# TODO: getting the correct JSON format throws exceptions when not using the correct model -> catch exception in parse JSON?
# TODO: KeyboardInterrupt when hypothesis exiting should exit the whole program using sys.exit()
# TODO: if spec is defined but the function never called, print something out as warning?

# ISSUE: if all functions are contained within a class, it won't be included in globals

# TODO: can't grab the class that a function is in 

# ISSUE: when I give it the qualname (e.g. Point.get_x(), it generates point in addition)
# ISSUE: when it calls init, there's inifite recursion

# IDEA: get expected and actual out of tests

cdb = database.CodeDatabase('pythoness-cache.db')

def spec(string, model="gpt-4o", replace=False, tests=None, max_retries=3, verbose=False, output=False, regenerate=False, related_objs=None, e_print = False, timeout_seconds=0):
    ''' Main logic of Pythoness '''
    def decorator(func):
        cached_function = None
        
        log = logger.Logger()
        
        func.__doc__ += string

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
                
                # Here is the infinite recursion

                if cached_function:
                    return cached_function(*args, **kwargs)

                client = assistant.Assistant(model=model)

                # We need to generate a function from the spec.
                # We populate the prompt with the function's name, argument name and types, and the return type.

                with log("[Pythoness] Getting function info...") if verbose else nullcontext():
                    # function_info = helper_funcs.get_function_info(func, *args, **kwargs)
                    function_info = helper_funcs.get_function_info(func)

                with log("[Pythoness] Creating prompt and checking the DB...") if verbose else nullcontext():
                    prompt = prompt_helpers.create_prompt(function_info, string, tests, func, related_objs)
                    function_info = helper_funcs.setup_info(function_info, func, string, prompt)

                # See if we already have code corresponding to that prompt in the database.
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
                            import inspect
                            frame = inspect.currentframe()
                            
                            with log("[Pythoness] Replacing...") if verbose else nullcontext(): 
                                helper_funcs.replace_func(frame, func, function_def)

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
                            # need to remove the new function from the global namespace that exec put it in
                            
                            
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
                                import inspect
                                frame = inspect.currentframe()
                                
                                with log("[Pythoness] Replacing...") if verbose else nullcontext():   
                                        helper_funcs.replace_func(frame, func, function_info['function_def'])
                                
                            return cached_function(*args, **kwargs)
                        
                        except Exception as e:
                            prompt = helper_funcs.exception_handler(e, verbose, log, e_print)
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
                                log.log(f"\n[Total Cost: ~${client.get_stats('cost'):.2f} USD]")

                # If we got here, we had too many retries.
                # ensure that nothing is in the DB to interfere with a future call
                cdb.delete_code(function_info["original_prompt"])
                raise Exception(f'Maximum number of retries exceeded ({max_retries}).')
        return wrapper
    return decorator

