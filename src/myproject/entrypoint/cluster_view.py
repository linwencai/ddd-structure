from logging import getLogger

from sanic import Blueprint
from sanic import HTTPResponse, Request, json
from sanic_ext import openapi, validate
from sanic_ext.extensions.openapi.definitions import RequestBody, Response, Parameter

from myproject.entrypoint import cluster_appserv
from ..message.request import CreateClusterRequest, UpdateClusterRequest, ListRequest
from ..message.response import ClusterResponse, ClusterListResponse

bp = Blueprint("resourcemanager", url_prefix="/rs")
logger = getLogger("myproject")


@bp.post("/cluster")
@openapi.definition(
    body=RequestBody(CreateClusterRequest, required=True),
    summary="创建 cluster",
    tag="cluster",
    response=[Response(ClusterResponse, status=200)],
)
@validate(json=CreateClusterRequest)
async def create_cluster(request: Request, body: CreateClusterRequest) -> HTTPResponse:
    app_service = cluster_appserv.ClusterAppService()
    cluster_response = await app_service.create_cluster(body)
    if cluster_response:
        return json(cluster_response.dict())
    else:
        return json({})


@bp.delete("/cluster/<cluster_id:int>")
@openapi.definition(
    summary="删除 cluster",
    tag="cluster",
    response=[Response(ClusterResponse, status=200)],
)
async def delete_cluster(request: Request, cluster_id: int) -> HTTPResponse:
    body = UpdateClusterRequest(is_alive=False)
    app_service = cluster_appserv.ClusterAppService()
    cluster_response = await app_service.update_cluster(cluster_id, body)
    if cluster_response:
        return json(cluster_response.dict())
    else:
        return json({})


@bp.post("/cluster/<cluster_id:int>")
@openapi.definition(
    body=RequestBody(UpdateClusterRequest, required=True),
    summary="修改 cluster",
    tag="cluster",
    response=[Response(ClusterResponse, status=200)],
)
@validate(json=UpdateClusterRequest)
async def update_cluster(request: Request, cluster_id: int, body: UpdateClusterRequest) -> HTTPResponse:
    app_service = cluster_appserv.ClusterAppService()
    cluster_response = await app_service.update_cluster(cluster_id, body)
    if cluster_response:
        return json(cluster_response.dict())
    else:
        return json({})


@bp.get("/cluster/<cluster_id:int>")
@openapi.definition(
    summary="查询单个 cluster",
    tag="cluster",
    response=[Response(ClusterResponse, status=200)],
)
async def get_cluster(request: Request, cluster_id: int) -> HTTPResponse:
    app_service = cluster_appserv.ClusterAppService()
    cluster_response = await app_service.get_cluster_by_id(cluster_id)
    if cluster_response:
        return json(cluster_response.dict())
    else:
        return json({})


@bp.get("/clusters")
@openapi.definition(
    parameter=Parameter("get_cluster_list", ListRequest, required=True),
    summary="获取多个 cluster",
    tag="cluster",
    response=[Response(ClusterListResponse, status=200)],
)
async def get_cluster_list(request: Request, parameter: ListRequest = None) -> HTTPResponse:
    if parameter is None:
        parameter = ListRequest()
    app_service = cluster_appserv.ClusterAppService()
    cluster_response = await app_service.get_cluster_list(parameter)
    if cluster_response:
        return json(cluster_response.dict())
    else:
        return json({})
