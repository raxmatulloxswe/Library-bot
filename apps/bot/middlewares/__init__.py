from .logging import *


def setup_middlewares(dp):
    dp.update.outer_middleware(LoggingMiddleware())
