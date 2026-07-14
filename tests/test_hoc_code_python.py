from conftest import run_script


def test_script_runs_without_error():
    output = run_script("Hoc_code_python.py")
    assert output


def test_print_with_custom_end():
    # print("Tôi là học sinh lớp 1", end="năm nay tôi 18 tuổi")
    output = run_script("Hoc_code_python.py")
    assert "Tôi là học sinh lớp 1năm nay tôi 18 tuổi" in output


def test_local_vs_global_scope_behavior():
    output = run_script("Hoc_code_python.py")
    # Inside the function the local x is used -> "Python is fantastic"
    assert "Python is fantastic" in output
    # Outside the function the global x remains -> "Python is awesome"
    assert "Python is awesome" in output


def test_global_keyword_modifies_outer_variable():
    output = run_script("Hoc_code_python.py")
    # concho() sets global x = "dumaSaiGon"
    assert "dumaSaiGon" in output
    # dumamay() then overrides it via the global keyword
    assert "mày có đẹp trai đéo đâu" in output
