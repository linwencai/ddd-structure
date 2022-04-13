import asyncio
from datetime import datetime
from functools import partial
from sanic import Blueprint
from sanic import Request, json, Sanic
from sanic_ext import openapi, validate, serializer
from sanic_ext.extensions.openapi.definitions import RequestBody, Response, Parameter

from diting.core.common.log import app_logger as logger

bp = Blueprint("system-controller", url_prefix="/sys/internal")

@bp.post("/log/level/<level:int>")
async def set_log_level(request, level:int):

    app : Sanic = request.app
    old_log_level = request.app.config.get("log")['level']
    new_log_level = old_log_level
    redis = request.app.ctx.redis

    check_log_level_config = app.config.get("scheduler")['check_log_level']
    check_key = check_log_level_config['check_key']
    interval = check_log_level_config['interval']
    
    await redis.set(check_key, level)
    
    for i in range(interval+1):
        new_log_level = request.app.config.get("log")['level']
        if new_log_level != level:
            await asyncio.sleep(1)
            continue
    result_flag = "Success" if new_log_level == level else "Failed"
    logger.info(f"{result_flag}. Try switch from {old_log_level} to {level}, now is {new_log_level}")

    return json({"msg" : f"{result_flag}. Try switch from {old_log_level} to {level}, now is {new_log_level}"})

@bp.get("/log/config")
async def get_log_config(request):

    log_config = request.app.config.get("log")

    return json(log_config)

@bp.get("/schedulers")
async def get_scheduler(request):
    scheduler = request.app.ctx.scheduler
    
    jobs = scheduler.get_jobs()
    logger.info(jobs)
    return json({"jobs" : str(jobs)})
