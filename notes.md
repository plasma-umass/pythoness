TODOs:
* verify that models other than OpenAI's work correctly
* use sys.exit() (or something else) when ctrl-c-ing in the middle of hypothesis testing,
so that the entire program exits instead of just that test
* add the ability to include specific unittests as strings which are TestCase or test module names;
it will use unittest.TestLoader.loadTestsFromName() to load them; additionally use regexes to determine which strings are individual tests
and which are unittests
* get expected and actual out of tests -> convert every test to unittests and use their assertions?
* verify that failing `max_retries` when unittests start generating code exits the program entirely; same with ctrl-c

QUESTIONS:
* when `verbose=True` and a test relies on stdout output, my pythoness verbose output is included; is there a way to only include non-pythoness generated output?
* using `'cls'` in `related_objs` when the spec defines a global function is undefined
behavior; currently it just adds the specified function once
* does adding an anthropomorphizing line at the beginning of the prompt (e.g. `'You are an expert python programmer...'`) increase consistency?
* can I increase testing coverage by having the LLM generate its own tests?