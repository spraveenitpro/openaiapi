from tenacity import *

@retry
def exception_function():
    print("Exception time!! 💣")
    raise Exception

@retry(stop=stop_after_attempt(5))
def max_attempts_function():
    print("Run 5 times")
    raise Exception

@retry(wait=wait_fixed(2))
def fixed_wait_function():
    print("Wait 2 seconds")
    raise Exception


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fixed_wait_and_max_attempts_function():
    print("Wait 2 seconds and run 3 times")
    raise Exception


@retry(wait=wait_random_exponential(multiplier=1, max=10))
def exponential_wait_function():
    print("Wait 1 to 60 seconds")
    raise Exception


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def exponential_wait_and_max_attempts_function():
    print("Wait 1 to 60 seconds and run 3 times")
    raise Exception

@retry(stop=stop_after_attempt(3), retry=retry_if_exception_type((IOError, ConnectionError)))
def different_exception_possible(x):
    if x == 1:
        print("IO error because x is 1")
        raise IOError
    elif x == 2:
        print("Connection error because x is 2")
        raise ConnectionError
    elif x == 3:
        print("Timeout error because x is 3")
        raise TimeoutError
    else:
        return "Success"


different_exception_possible(4)