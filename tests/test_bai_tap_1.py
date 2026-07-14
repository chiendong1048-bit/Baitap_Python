from conftest import run_script


def test_rectangle_dimensions_are_reported():
    output = run_script("bai_tap_1.py")
    assert "Chieu dai hinh chu nhat la: 10" in output
    assert "Chieu rong hinh chu nhat la: 5" in output


def test_area_and_perimeter_are_correct():
    # dien_tich = 10 * 5 = 50 ; chu_vi = (10 + 5) * 2 = 30
    output = run_script("bai_tap_1.py")
    assert "Dien tich hinh chu nhat la: 50" in output
    assert "Chu vi hinh chu nhat la: 30" in output
