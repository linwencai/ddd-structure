import logging
from sanic import Request, Sanic, exceptions, json

app = Sanic.get_app()
logger = logging.getLogger("diting")


@app.exception(exceptions.NotFound)
async def not_fount(request: Request, exception: exceptions.SanicException):
    """
    自定义 404 返回值
    :param request:
    :param exception:
    :return:
    """
    logger.error(f"not_fount request=%s exception=%s", request, exception)
    return json({"status": 404, "message": str(exception)}, 404)


@app.exception(exceptions.SanicException)
async def sanic_exception(request: Request, exception: exceptions.SanicException):
    """
    自定义 sanic 异常响应
    :param request:
    :param exception:
    :return:
    """
    status_code = exception.status_code or 500
    if status_code < 500:
        logger.error(f"sanic_exception request=%s, exception=%s", request, exception)
    else:
        logger.exception(f"sanic_exception request=%s, exception=%s", request, exception)
    return json({"status": status_code, "message": str(exception)}, status_code)


@app.exception(Exception)
async def base_exception(request: Request, exception: Exception):
    """
    自定义 异常响应
    :param request: 请求
    :param exception: 异常
    :return: HTTPResponse
    """
    logger.exception(f"base_exception request=%s, exception=%s", request, exception)
    status_code = 500
    return json({"status": status_code, "message": str(exception)}, status_code)
