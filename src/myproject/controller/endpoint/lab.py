from logging import getLogger
from typing import Awaitable, Callable, List

from sanic import Blueprint, HTTPResponse, Request, json
from sanic.exceptions import NotFound

bp = Blueprint("Lab", url_prefix="/lab")
logger = getLogger("myproject")


@bp.get("/")
async def get(request: Request) -> HTTPResponse:
    logger.info("hello hello")
    return json({"hello" : "world"})
