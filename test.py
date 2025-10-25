import time


def time_it(func):
    print("I'm outter")

    def wrapper(*args, **kwargs):
        start_tiem = time.perf_counter()
        res = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"函数 {func.__name__} 运行时间: {end_time - start_tiem} 秒")
        return res

    return wrapper


# time_it(test)
@time_it
def test():
    print("test")


test()
