from conftest import run_script


def test_script_runs_without_error():
    output = run_script("Pythondatatypes.py")
    assert output


def test_camping_list_length():
    # campinglist has 5 elements (duplicates allowed)
    output = run_script("Pythondatatypes.py")
    assert "5" in output.splitlines()


def test_total_score_after_append_and_update():
    # diem_so = [8.5, 9.0, 7.5] -> append(10) -> [0] = 9.5 => [9.5, 9.0, 7.5, 10]
    # sum = 36.0
    output = run_script("Pythondatatypes.py")
    assert "36.0" in output.splitlines()


def test_updated_profile_age():
    # profile["tuoi"] starts at 17 then += 1 => 18, and status is added
    output = run_script("Pythondatatypes.py")
    assert "Đang hoạt động" in output
    assert "'tuoi': 18" in output
