from tools.plugins import RunnerPlugin


SOLUTION_TEMPLATE_FILEPATH = "solution_template.py"
SOLUTION_TESTER_FILEPATH = "solution_pytester.py"


class PythonRunner(RunnerPlugin):

    lang = "python"
