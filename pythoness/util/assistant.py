import textwrap
import time
import litellm
import openai


class AssistantError(Exception):
    """A custom exception to catch wrong model issues"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Assistant:
    def __init__(
        self,
        model="gpt-4o",
    ):
        self._model = model
        self._stats = {}
        self._history = []
        # streaming will be enabled later
        self._check_model()

    def _warn_about_exception(self, e: Exception, message: str) -> None:
        """Formats and prints exception information"""
        import traceback

        tb_lines = traceback.format_exception(type(e), e, e.__traceback__)
        tb_string = "".join(tb_lines)
        print(f"{message}\n\n{e}\n{tb_string}")

    def query(self, prompt: str) -> str:
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

        except openai.OpenAIError as e:
            self._warn_about_exception(e, f"Unexpected OpenAI Error.  Retry the query.")
            return

        except Exception as e:
            self._warn_about_exception(e, f"Unexpected Exception.")

        return result

    def get_stats(self, stat: str):
        """Gets the stat 'stat' from the self._stats dictionary"""
        return self._stats[stat]

    def _check_model(self) -> None:
        """Verifies the API key in environment variables"""

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

    def _batch_query(self, prompt: str) -> str:
        """Gets cost and returns the string from a completion"""
        completion = self._completion(prompt)
        self._stats["cost"] += litellm.completion_cost(completion)

        response_message = completion.choices[0].message.content

        return response_message

    def _completion(self, user_prompt: str) -> litellm.ModelResponse:
        """Returns an LLM completion and appends the prompt and result to self._history"""
        self._history.append({"role": "user", "content": user_prompt})
        completion = litellm.completion(
            model=self._model,
            messages=self._history,
            response_format={"type": "json_object"},
        )
        self._history.append(
            {"role": "assistant", "content": completion.choices[0].message.content}
        )
        return completion
