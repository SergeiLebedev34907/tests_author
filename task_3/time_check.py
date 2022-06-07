import time


def time_check(func):
    def wrapper(*args):
        start_time = time.time()
        result = func(*args)
        execution_time = round(time.time() - start_time, 1)
        print(f'Время выполнения функции: {execution_time} с.')
        return result

    return wrapper
