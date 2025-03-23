# test_factorial.py - pytest 스타일의 테스트 코드
import pytest
from factorials import factorial

def test_factorial_basic():
    # 일반 사례: 5! = 120, 그리고 0! = 1, 1! = 1
    assert factorial(5) == 120
    assert factorial(1) == 1
    assert factorial(0) == 1

def test_factorial_negative():
    # 음수 입력 시 예외 발생 여부 확인
    with pytest.raises(ValueError):
        factorial(-3)