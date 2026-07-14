from conftest import run_script


def test_sum_and_product_messages():
    output = run_script("tinhtoan.py")
    assert "Tổng của a và b là: 15" in output
    assert "Tích của a và b là: 50" in output


def test_arithmetic_operations_on_10_and_3():
    output = run_script("tinhtoan.py")
    lines = output.splitlines()
    # After the two Vietnamese messages, a=10 and b=3 are printed in order:
    # a + b, a * b, a ** b, a % b, a / b, a - b
    assert "13" in lines          # 10 + 3
    assert "30" in lines          # 10 * 3
    assert "1000" in lines        # 10 ** 3
    assert "1" in lines           # 10 % 3
    assert "7" in lines           # 10 - 3
    assert any(line.startswith("3.33") for line in lines)  # 10 / 3
