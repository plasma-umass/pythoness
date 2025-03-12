The pythoness/eval/results directory contains a subdirectory for each problem id number. Within each is:
* "[id]_problem.json" Contains the JSON returned by the GET request for the problem description, details, and template code.
* "[id]_config[config#].py" The Python file containing the problem function to be fed into Pythoness, wrapped in the Pythoness decorator and with tests and Pythoness specs formatted according to desired Pythoness configuration.
* "[id]_config[config#]_[#].py" The Python code produced by the LLM on iteration [#], whose output matches the info captured in "[id]_config[config#].out" This code is what is passed to LeetCode for eval.
* "[id]_config[config#].out" The Pythoness stdout log for all runs under a single config
* "[id]_config[config#]_[#].txt" Contains the Python code being passed to the LeetCode judge for the [#] solution submission.
* "[id]_config[config#]_[#].json" Contains the LeetCode submission results for the corresponding .py and .txt files.

All steps but the first must be repeated for 4 different configs of Pythoness.