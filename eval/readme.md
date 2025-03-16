The pythoness/eval/results/ directory contains a subdirectory for each problem id number. Each problem subdirectory contains the following:

Problem Generation files:
* "p[id]_problem.json" The JSON returned by the GET request for the problem description, details, and template code.
* "p[id]_config[config#].py" The Python file containing the problem function to run Pythoness, wrapped in the Pythoness decorator and with tests and Pythoness specs formatted according to desired Pythoness configuration.
* "p[id]_config[config#]_[#].py" The code produced by Pythoness on iteration [#].
* "p[id]_config[config#].out" The Pythoness stdout log for all runs under a single config.

Testing files:
* "src/p[id]oracle.py" The ground truth Python code, taken from either (1) LeetCode (2) leetcode (3) LeetCode discussion boards
* "tests/test_coverup_*.py" The pytest tests produced by Coverup
* "coverup-log" The log produced by Coverup containing function call details
* "test_coverup_*.py" Copies of the pytest results placed in the parent directory so that Coverup can be rerun if necessary, but also so that pytest will run properly with ground truth and other implementations
