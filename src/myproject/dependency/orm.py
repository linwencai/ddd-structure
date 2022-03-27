
import urllib.parse
from sanic import Sanic
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

app = Sanic.get_app()

def get_orm_dsn(options):

    dialect = options.get("dialect")
    driver = options.get("driver")
    username = options.get("username")
    password = options.get("password")
    host = options.get("host")
    port = options.get("port")
    database = options.get("database")
    parsed_password_url = urllib.parse.quote_plus(password)

    if dialect == "sqlite":
        if driver is None:
            return f"{dialect}:///{database}"
        else:
            return f"{dialect}+{driver}:///{database}"

    return f"{dialect}+{driver}://{username}:{parsed_password_url}@{host}:{port}/{database}"

_base_model_session_ctx = ContextVar("orm_session")

@app.before_server_start
async def setup_orm_engine(app: Sanic, _) -> None:
    dsn = get_orm_dsn(app.config.get("database"))
    app.ctx.orm_engine = create_async_engine(dsn)

@app.on_request
async def inject_session(request):
    request.ctx.orm_session = sessionmaker(app.ctx.orm_engine, AsyncSession, expire_on_commit=False)()
    request.ctx.orm_session_ctx_token = _base_model_session_ctx.set(request.ctx.orm_session)

@app.on_response
async def close_session(request, response):
    if hasattr(request.ctx, "orm_session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.orm_session_ctx_token)
        await request.ctx.orm_session.close()