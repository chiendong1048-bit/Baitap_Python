import random

from conftest import run_script


def test_script_runs_without_error():
    # Uses random.randrange internally; seed for determinism/reproducibility.
    random.seed(0)
    output = run_script("biencuapython.py")
    assert output


def test_string_concatenation_and_fstring():
    random.seed(0)
    output = run_script("biencuapython.py")
    assert "Hello World" in output
    assert "Tên tôi là Đồng Tố Chiến, Năm nay tôi 20 tuổi" in output


def test_membership_and_slicing_outputs():
    random.seed(0)
    output = run_script("biencuapython.py")
    lines = output.splitlines()
    # print("trader" in text) -> True ; print("hello" in text) -> False
    assert "True" in lines
    assert "False" in lines
    # text[2:5] of "Hello world!" -> "llo"
    assert "llo" in lines


def test_split_produces_expected_list():
    random.seed(0)
    output = run_script("biencuapython.py")
    # raw_data "BTC;64000;2024-04-08" split on ";"
    assert "['BTC', '64000', '2024-04-08']" in output
