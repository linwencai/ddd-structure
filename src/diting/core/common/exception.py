import traceback
from sanic import Request, Sanic, exceptions, json
from diting.core.common.log import app_logger as logger

app = Sanic.get_app()

def format_exception(exception: Exception):
    return traceback.format_exception(type(exception), exception, exception.__traceback__)

@app.exception(exceptions.NotFound)
async def not_found(request: Request, exception: exceptions.SanicException):
    """
    自定义 404 返回值
    :param request:
    :param exception:
    :return:
    """
    logger.warning(f"not_found request=%s exception=%s", request, exception)
    status_code = 404
    return json(
        {
            "code": status_code,
            "detail": format_exception(exception),
            "data": {},
            "msg": "resource not found",
        },
        status_code
    )


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
    return json(
        {
            "code": status_code,
            "detail": format_exception(exception),
            "data": {},
            "msg": str(exception),
        },
        status_code,
    )

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
    return json(
        {
            "code": status_code,
            "detail": format_exception(exception),
            "data": {},
            "msg": str(exception),
        },
        status_code,
    )
