
import urllib.parse
from sanic import Sanic
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from diting.core.common.context import base_model_session_ctx
from diting.lrm.adapter import table_schema

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
            return f"{dialect}://{database}"
        else:
            return f"{dialect}+{driver}://{database}"

    return f"{dialect}+{driver}://{username}:{parsed_password_url}@{host}:{port}/{database}"


@app.before_server_start
async def setup_orm_engine(app: Sanic, _) -> None:
    dsn = get_orm_dsn(app.config.get("database"))
    app.ctx.orm_engine = create_async_engine(dsn)
    # app.ctx.orm_engine = create_engine(dsn)


# @app.after_server_start
# async def setup_orm_mapper(app: Sanic, _) -> None:
#     table_schema.start_mappers()


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
        # request.ctx.orm_session.close()

# ----------------------------------------------------------- #
from diting.lrm.domain.cluster_model import ClusterModel
from diting.core.base.table import mapper_registry
from diting.lrm.adapter.table_schema import cluster_table

mapper_registry.map_imperatively(ClusterModel, cluster_table)