# 封装系统调用的一些逻辑
import logging
from sanic import Sanic
from diting.core.common.log import set_logger_level
from diting.core.common.log import app_logger as logger
from diting.core.module.scheduler import scheduler_at

# id 参数是必填的， 参数就是apscheduler 的 add_job 参数
# 任务可以是定时相关的逻辑，也可以是发布一个事件，参考 sanic signal
@scheduler_at("interval", seconds=5, id="check_logger_level")
async def check_logger_level(app: Sanic):
    current_log_level = app.config.get("log")['level']
    logger.debug(f"current log level is {logging.getLevelName(current_log_level)}")

    if not hasattr(app.ctx, "redis"):
        return
    redis = app.ctx.redis
    key = app.config.get("scheduler")['check_log_level']['check_key']

    try:
        new_log_level = await redis.get(key)
    except Exception as e:
        logger.error("can't connect to redis, please check!")
        return

    if(new_log_level):
        if current_log_level != int(new_log_level):
            set_logger_level(app, int(new_log_level))