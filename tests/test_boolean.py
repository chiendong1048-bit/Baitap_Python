from conftest import run_script


def test_boolean_script_runs_without_error():
    output = run_script("boolean.py")
    assert output  # produced some output


def test_comparison_results():
    output = run_script("boolean.py")
    lines = output.splitlines()
    # print(10 > 9) -> True ; print(5 == 3) -> False ; print(9 < 8) -> False
    assert lines[0] == "True"
    assert lines[1] == "False"
    assert lines[2] == "False"


def test_else_branch_and_function_return():
    # b (100) is not greater than a (500) -> else branch is taken
    output = run_script("boolean.py")
    assert "b is not greater than a" in output
    # def myfunction(): return True -> "Yes!" branch
    assert "Yes!" in output
