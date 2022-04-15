
import urllib.parse
import copy
from sanic import Sanic
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from diting.core.common.context import base_model_session_ctx
from diting.lrm.adapter import table_schema

app = Sanic.get_app()

def get_orm_dsn(config):

    options = copy.deepcopy(config)

    dialect = options.pop("dialect")
    driver = options.pop("driver")
    username = options.pop("username")
    password = options.pop("password")
    host = options.pop("host")
    port = options.pop("port")
    database = options.pop("database")
    charset = options.pop("charset")

    parsed_password_url = urllib.parse.quote_plus(password)

    if dialect == "sqlite":
        if driver is None:
            return f"{dialect}://{database}", {}
        else:
            return f"{dialect}+{driver}://{database}", {}

    return f"{dialect}+{driver}://{username}:{parsed_password_url}@{host}:{port}/{database}?charset={charset}", options 


@app.before_server_start
async def setup_orm_engine(app: Sanic, _) -> None:
    dsn, opt = get_orm_dsn(app.config.get("database"))
    app.ctx.orm_engine = create_async_engine(dsn, **opt)

@app.on_request
async def inject_session(request):
    request.ctx.orm_session = sessionmaker(app.ctx.orm_engine, AsyncSession, expire_on_commit=False)()
    # request.ctx.orm_session = sessionmaker(app.ctx.orm_engine, Session, expire_on_commit=False)()
    request.ctx.orm_session_ctx_token = base_model_session_ctx.set(request.ctx.orm_session)

@app.on_response
async def close_session(request, response):
    if hasattr(request.ctx, "orm_session_ctx_token"):
        base_model_session_ctx.reset(request.ctx.orm_session_ctx_token)
        await request.ctx.orm_session.close()
