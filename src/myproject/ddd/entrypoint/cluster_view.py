from logging import getLogger

from sanic import Blueprint
from sanic_ext.extensions.openapi.definitions import RequestBody, Response
from sanic_ext import openapi
from sanic import HTTPResponse, Request, json
from sqlalchemy import update

from myproject.ddd.domain.cluster_model import Cluster
from myproject.ddd.entrypoint import cluster_appserv
from ..message.response import ClusterResponse
from ..message.request import CreateClusterRequest, UpdateClusterRequest
from sanic_ext import validate

bp = Blueprint("resourcemanager", url_prefix="/rs")
logger = getLogger("myproject")


@bp.put("/cluster")
@openapi.definition(
    body=RequestBody(UpdateClusterRequest, required=True),
    summary="create_cluster",
    tag="cluster",
    response=[Response(UpdateClusterRequest, status=200)],
)
@validate(json=CreateClusterRequest)
async def update_cluster(request: Request, body: UpdateClusterRequest) -> HTTPResponse:
    appservice = cluster_appserv.ClusterAppService()
    cluster_response = appservice.update_cluster(body)
    if cluster_response:
        return json(cluster_response.to_dict())
    else:
        return json({})


@bp.post("/cluster")
@openapi.definition(
    body=RequestBody(CreateClusterRequest, required=True),
    summary="create_cluster",
    tag="cluster",
    response=[Response(ClusterResponse, status=200)],
)
@validate(json=CreateClusterRequest)
async def create_cluster(request: Request, body: CreateClusterRequest) -> HTTPResponse:
    appservice = cluster_appserv.ClusterAppService()
    cluster_response = appservice.create_cluster(body)
    if cluster_response:
        return json(cluster_response.to_dict())
    else:
        return json({})


@bp.get("/cluster/<id:int>")
@openapi.definition(
    summary="get_cluster",
    tag="cluster",
    response=[Response(ClusterResponse, status=200)],
)
async def get_cluster(request: Request, id: int) -> HTTPResponse:
    appservice = cluster_appserv.ClusterAppService()
    cluster_response = appservice.get_cluster_by_id(id)
    if cluster_response:
        return json(cluster_response.to_dict())
    else:
        return json({})

