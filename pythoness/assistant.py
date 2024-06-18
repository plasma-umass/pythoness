import textwrap
import time
import litellm
import openai

class AssistantError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Assistant:
    def __init__(
        self,
        model="gpt-4",
    ):
        self._model = model
        self._stats = {}
        # streaming will be enabled later
        self._check_model()

    def _warn_about_exception(self, e, message="Unexpected Exception"):
        import traceback

        tb_lines = traceback.format_exception(type(e), e, e.__traceback__)
        tb_string = "".join(tb_lines)
        print(tb_string)
        
    def query(self, prompt: str):
        """
        Sends prompt to the LLM and returns the resulting text
        
        Updates a dictionary containing
            - "completed": True if the query ran to completion
            - "cost": Cost of the query, or 0 if not completed
        Other fields only if completed is True
            - "time":               completion time in seconds
            - "model":              the model used
        """
        self._stats = {"completed": False, "cost": 0}
        start = time.time()
            
        try:
            result = self._batch_query(prompt)

            elapsed = time.time() - start

            self._stats["time"] = elapsed
            self._stats["model"] = self._model
            self._stats["completed"] = True
            self._stats["message"] = f"\n[Cost: ~${self._stats['cost']:.2f} USD]"

        except openai.OpenAIError as e:
            self._warn_about_exception(e, f"Unexpected OpenAI Error.  Retry the query.")
            self._stats["message"] = f"[Exception: {e}]"
            return

        except Exception as e:
            self._warn_about_exception(e, f"Unexpected Exception.")
            self._stats["message"] = f"[Exception: {e}]"
            
        return result

    def get_stats(self, stat):
        return self._stats[stat]

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
        
    def _batch_query(self, prompt: str):
        cost = 0
                            
        completion = self._completion(prompt, [])
        cost += litellm.completion_cost(completion)

        response_message = completion.choices[0].message.content

        self._stats['cost'] = cost
    
        return response_message

    def _completion(self, user_prompt: str, history: list):
        history.append({"role": "user", "content": user_prompt})
        completion = litellm.completion(
            model=self._model, # args["llm"]
            messages=history,
        )
        history.append({"role": "assistant", "content": completion.choices[0].message.content})
        return completion
