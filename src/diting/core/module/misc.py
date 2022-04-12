
from sanic import Request, Sanic
from diting.core.common.log import log_update_hostname_pid
from diting.core.common.context import base_request_ctx

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