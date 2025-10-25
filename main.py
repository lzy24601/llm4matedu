# from llms.llm_api import test_log
from utils.log_it import log_function_call

"""
装饰器有无括号的区别
无括号
@dec
def f():
    pass
等价于 f = dec(f)

有括号
@dec(x)
def f():
    pass
等价于 f = dec(x)(f)
"""


@log_function_call()
def main():
    # print()
    # test_log()
    print("hello")
    return 1


if __name__ == "__main__":
    main()
