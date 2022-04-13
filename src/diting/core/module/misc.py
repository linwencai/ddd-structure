import diting.core.common.exception
from sanic import Request, Sanic
from diting.core.common.log import log_update_hostname_pid
from diting.core.common.context import base_request_ctx
from diting.core.common.log import app_logger as logger

app: Sanic = Sanic.get_app()


@app.after_server_start
async def setup_request_context(app: Sanic, _) -> None:
    app.ctx.request = base_request_ctx
    
@app.on_request
async def attach_request(request: Request) -> None:
    # 每次请求进来时，注入request对象
    request.ctx.request_ctx_token = base_request_ctx.set(request)

@app.on_response
async def detach_request(request, response):
    if hasattr(request.ctx, "request_ctx_token"):
        base_request_ctx.reset(request.ctx.request_ctx_token)


@app.before_server_start
async def change_logger_pid(app: Sanic, _) -> None:
    log_update_hostname_pid()

@app.after_server_start
async def init_snowflake_id(app: Sanic, _) -> None:
    from diting.core.common.snowflake import snowflake, generate_snowflake_id
    instance_num = snowflake.instance
    if hasattr(app.ctx, "redis"):
        redis = app.ctx.redis
        logger.info("Using redis to generate unique snowflake instance")
        try:
            instance_num = await redis.incr("__snowflake_instance_num__")
            snowflake.set_instance(instance_num)
        except:
            logger.error("setup snowflake-redis failed, due to redis error")
    else:
        logger.info("Using default unique snowflake instance")
    logger.info(f"snowflake instance {instance_num}, next id is {generate_snowflake_id()}")