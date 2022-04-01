from contextvars import ContextVar

from sanic import Request, Sanic
from myproject.ddd.south.adapter.repository.cluster import cluster_table

app = Sanic.get_app()


@app.after_server_start
async def setup_request_context(app: Sanic, _) -> None:
    # 注入 request 值，方便 log 模块登记 request.id 进行链路跟踪
    app.ctx.request = ContextVar("request")

    cluster_table.start_mappers()


@app.on_request
async def attach_request(request: Request) -> None:
    # 每次请求进来时，注入request对象
    request.app.ctx.request.set(request)