def divide(a: float, b: float) -> float:
    """a를 b로 나눈 결과를 반환한다. 0으로 나누는 경우 ValueError 발생."""
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b