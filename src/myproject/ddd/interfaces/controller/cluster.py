from logging import getLogger

from sanic import Blueprint, HTTPResponse, Request, json
from sanic.exceptions import NotFound
from sanic.views import HTTPMethodView
from sqlalchemy import select, update

# /api/v1/rs

bp = Blueprint("resourcemanager", url_prefix="/rs")
logger = getLogger("myproject")

from myproject.ddd.interfaces.dto.resource import Cluster

@bp.put("/cluster")
async def update_cluster(request: Request) -> HTTPResponse:
    session = request.ctx.orm_session
    async with session.begin():

        stmt = update(Cluster).where(Cluster.id == request.json['id']).values(**request.json)
        await session.execute(stmt)
        await session.commit()
        
    return json(request.json)

@bp.post("/cluster")
async def create_cluster(request: Request) -> HTTPResponse:
    session = request.ctx.orm_session
    async with session.begin():
        obj = Cluster(**request.json)
        session.add(obj)
        await session.commit()
        
    return json(obj.to_json())

@bp.get("/cluster/<id:str>")
async def get(request: Request, id: int) -> HTTPResponse:
    session = request.ctx.orm_session

    async with session.begin():
        stmt = select(Cluster).where(Cluster.id == id)
        result = await session.execute(stmt)
        cluster = result.scalar()
    
    if not cluster:
        return json({})

    return json(cluster.to_json())
