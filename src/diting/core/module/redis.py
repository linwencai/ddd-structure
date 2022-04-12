import copy
import aioredis
from sanic import Sanic
from diting.core.common.log import app_logger as logger

app = Sanic.get_app()

def get_redis_dsn(config):
    options = copy.deepcopy(config)
    
    redis_type = options.pop("type")
    redis_dsn = options.pop("dsn")
    redis_host = options.pop("host")
    redis_schema = options.pop("schema")
        
    if redis_type == "Single":
        return redis_dsn.format(schema=redis_schema, host=redis_host), options

@app.before_server_start
async def setup_redis(app: Sanic, _) -> None:
    dsn, options = get_redis_dsn(app.config.get("redis"))
    app.ctx.redis = aioredis.from_url(dsn, **options)
    try:
        await app.ctx.redis.ping()
        app.ctx.redis_status = "running"
        logger.info(f"connect to redis successfully!")
    except:
        app.ctx.redis_status = "error"
        logger.error("setup redis error!")

@app.after_server_stop
async def shutdown_redis(app: Sanic, _) -> None:
    await app.ctx.redis.close()

async def reconnect_redis(app: Sanic):

    if hasattr(app.ctx, "redis"):
        if app.ctx.redis_status == "running":
            app.ctx.redis.close()
            app.ctx.redis_status = "stop"

    dsn, options = get_redis_dsn(app.config.get("redis"))
    app.ctx.redis = aioredis.from_url(dsn, **options)
    await app.ctx.redis.ping()
    logger.info(f"reconnect to redis successfully!")
    app.ctx.redis_status = "running"