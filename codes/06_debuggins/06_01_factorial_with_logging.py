import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def factorial(n: int) -> int:
    """n의 팩토리얼을 반환한다. n이 음수이면 ValueError 발생."""
    logging.debug(f"factorial({n}) 호출됨")
    if n < 0:
        logging.error("음수 값에 대한 팩토리얼은 정의되지 않습니다.")
        raise ValueError("음수 값에 대한 팩토리얼은 정의되지 않습니다.")
    if n <= 1:
        logging.debug(f"factorial({n}) = 1 반환")
        return 1
    result = n * factorial(n - 1)
    logging.debug(f"factorial({n}) = {result} 반환")
    return result

if __name__ == "__main__":
    try:
        logging.debug("factorial(5) 호출")
        print(factorial(5))  # 120
        logging.debug("factorial(0) 호출")
        print(factorial(0))  # 1
        logging.debug("factorial(-5) 호출")
        print(factorial(-5))  # ValueError: 음수 값에 대한 팩토리얼은 정의되지 않습니다.
    except ValueError as e:
        logging.exception("예외 발생: %s", e)
