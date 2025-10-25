from loguru import logger
from pathlib import Path
import functools

project_dir = Path(__file__).parent.parent
print(project_dir)
log_dir = project_dir / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "llm_api.log"

try:
    logger.remove()
    print(logger.__format__())
    logger.add(log_file, encoding="utf-8")
except Exception:
    pass


# 使用functools.wraps的装饰器
def log_function_call(level="INFO"):
    """使用@functools.wraps的日志装饰器"""

    def decorator(func):
        # 这里打印的是原始函数名
        print(f"装饰器接收到的函数名: {func.__name__}")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 这里仍然可以访问原始函数名
            logger.log(
                level, f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}"
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator
