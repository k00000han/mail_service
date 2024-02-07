import logging

from common import config


def setup_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d] - [%(funcName)s]",
        level=logging.DEBUG if config.DEBUG else logging.INFO,
    )


def get_logger(name):
    return logging.getLogger(name)


# def log_function(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         logging.info(f'Function {func.__name__} was called with args: {args}, kwargs: {kwargs}')
#         try:
#             result = func(*args, **kwargs)
#             logging.info(f'Function {func.__name__} executed successfully')
#             return result
#         except Exception as e:
#             logging.error(f'Error in function {func.__name__}: {e}', exc_info=True)
#     return wrapper


setup_logging()
