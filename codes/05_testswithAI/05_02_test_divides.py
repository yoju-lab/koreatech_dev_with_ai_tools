import pytest
from divides import divide

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (9, 3, 3),
    (5, 2, 2.5),
    (1, 1, 1),
    (0, 1, 0),
    (-10, 2, -5),
    (10, -2, -5),
    (-10, -2, 5),
    (2.5, 0.5, 5.0)
])
def test_divide(a, b, expected):
    assert divide(a, b) == expected

def test_divide_by_zero():
    with pytest.raises(ValueError, match="0으로 나눌 수 없습니다."):
        divide(1, 0)
