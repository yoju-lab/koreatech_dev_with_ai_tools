# factorial.py - 테스트 대상 함수 구현
def factorial(n: int) -> int:
    """n의 팩토리얼을 반환한다. n이 음수이면 ValueError 발생."""
    if n < 0:
        raise ValueError("음수 값에 대한 팩토리얼은 정의되지 않습니다.")
    if n <= 1:
        return 1
    return n * factorial(n - 1)