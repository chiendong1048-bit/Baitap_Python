from conftest import run_script


def test_hello_prints_expected_message():
    output = run_script("hello.py")
    assert "Hello AI FPTU - Toi da ket noi duoc Github" in output
