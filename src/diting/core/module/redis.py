import copy
from pickletools import optimize
import aioredis
from sanic import Sanic

app = Sanic.get_app("")

def get_redis_dsn(config):
    options = copy.deepcopy(config)
    
    redis_type = options.pop("type")
    redis_dsn = options.pop("dsn")
        
    if redis_type == "Single":
        return redis_dsn, options


@app.before_server_start
async def setup_redis(app: Sanic, _) -> None:
    dsn, options = get_redis_dsn(app.config.get("redis"))
    app.ctx.redis_pool = aioredis.BlockingConnectionPool.from_url(dsn, **options)
    app.ctx.redis = aioredis.Redis(connection_pool=app.ctx.redis_pool)


@app.after_server_stop
async def shutdown_redis(app: Sanic, _) -> None:
    await app.ctx.redis_pool.disconnect()