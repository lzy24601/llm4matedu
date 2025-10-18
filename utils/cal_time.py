import time


def timer(func):
    def wrapper(*args, **kwargs):
        stat_time = time.perf_counter()
        res = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"函数 {func.__name__} 运行时间: {end_time - stat_time} 秒")
        return res

    return wrapper
