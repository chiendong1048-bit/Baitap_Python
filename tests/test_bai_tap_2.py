from conftest import run_script


def test_quadratic_expression_value():
    # y = a*x^2 + b*x + c = 2*25 + 3*5 + 1 = 66
    output = run_script("bai_tap_2.py")
    assert "Giá trị của biểu thức y là: 66" in output
