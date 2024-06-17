import inspect
import json
import sys
import textwrap

import time


# copied from chatDBG, don't know if it's needed
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import litellm

import openai

class AssistantError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

# needed? perhaps for the debug/verbose printing?
import string
def remove_non_printable_chars(s: str) -> str:
    printable_chars = set(string.printable)
    filtered_string = "".join(filter(lambda x: x in printable_chars, s))
    return filtered_string



class Assistant:
    # TODO: make options modular
    def __init__(
        self,
        instructions,
        model="gpt-4o",
        timeout=30,
        # taken from DBG, needed? requires specific packages
        # listeners=[Printer()],
        functions=[],
        max_call_response_tokens=2048,
        debug=False,
        stream=False,
    ):
        
        # hide debugging info, it might mess with error handling
        litellm.suppress_debug_info = True
        litellm.set_verbose = False


            
        self._model = model
        self._timeout = timeout
        self._conversation = [{"role": "system", "content": instructions}]
        self._max_call_response_tokens = max_call_response_tokens
        # streaming will be properly enabled later

        self._check_model()







    def _warn_about_exception(self, e, message="Unexpected Exception"):
        import traceback

        tb_lines = traceback.format_exception(type(e), e, e.__traceback__)
        tb_string = "".join(tb_lines)
        print(tb_string)

        
    # largely taken from DBG
    def query(self, prompt: str, user_text):
        """
        Send a query to the LLM
            - prompt is the prompt to send
            - user_text is what the user gave (which will be included in prompt)
        
        Returns a dictionary containing
            - "completed": True if the query ran to completion
            - "cost": Cost of the query, or 0 if not completed
        Other field only if completed is True
            - "time":               completion time in seconds
            - "model":              the model used
            - "tokens":             total tokens
            - "prompt_tokens":      our prompts
                - "completion_tokens":  the LLM completions part
            """
        stats = {"completed": False, "cost": 0}
        start = time.time()

        # broadcast yet unwritten
        # self._broadcast("on_begin_query", prompt, user_text)
            
        try:
            stats = self._batch_query(prompt, user_text)

            elapsed = time.time() - start

            stats["time"] = elapsed
            stats["model"] = self._model
            stats["completed"] = True
            stats["message"] = f"\n[Cost: ~${stats['cost']:.2f} USD]"


        # TODO: Exceptions
        except openai.OpenAIError as e:
            self._warn_about_exception(e, f"Unexpected OpenAI Error.  Retry the query.")
            stats["message"] = f"[Exception: {e}]"
            return
            
        return stats
        

    def _report(self, stats):
        if stats["completed"]:
            print()
        else: print("[Chat Interrupted]")

    def _check_model(self):
        result = litellm.validate_environment(self._model)
        missing_keys = result["missing_keys"]
        if missing_keys != []:
            _, provider, _, _ = litellm.get_llm_provider(self._model)
            if provider == "openai":
                raise AssistantError(
                    textwrap.dedent(
                        f"""\
                    You need an OpenAI key to use the {self._model} model.
                    You can get a key here: https://platform.openai.com/api-keys.
                    Set the environment variable OPENAI_API_KEY to your key value.
                    """
                    )
                )
            else:
                raise AssistantError(
                    textwrap.dedent(
                        f"""\
                    You need to set the following environment variables
                    to use the {self._model} model: {', '.join(missing_keys)}.
                    """
                    )
                )
            
        # function errors go here

        # def _add_function?

        # def _make_call?

    def _batch_query(self, prompt: str, user_text):
        cost = 0
            
        self._conversation.append({"role": "user", "content": prompt})
                
        completion = self._completion()
        cost += litellm.completion_cost(completion)

        response_message = completion.choices[0].message
        self._conversation.append(response_message.json())

        stats = {
            "cost": cost,
            # "tokens": completion.usage.total_tokens,
            # "prompt_tokens": completion.usage.prompt_tokens,
            # "completion_tokens": completion.usage.completions_tokens
        }
        return stats
    
    def _test_completion(self, prompt):
        return litellm.completion(
            model=self._model,
            messages=self._conversation,
            timeout=self._timeout,
            logger_fn=None,
        )
        
    def _completion(self, stream=False):

        return litellm.completion(
            model=self._model,
            messages=self._conversation,
            timeout=self._timeout,
            logger_fn=None,
            stream=stream,
        )
    



            
    def _test_complete(self, user_prompt: str, history: list) -> str:
        history.append({"role": "user", "content": user_prompt})
        completion = litellm.completion(
            # For now, hard code
            model="gpt-4", # args["llm"]
            messages=history,
            logger_fn=None,
        )
        history.append({"role": "assistant", "content": completion.choices[0].message.content})
        return completion.choices[0].message.content
