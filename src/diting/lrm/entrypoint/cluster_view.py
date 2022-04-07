from logging import getLogger

from sanic import Blueprint
from sanic import HTTPResponse, Request, json
from sanic_ext import openapi, validate
from sanic_ext.extensions.openapi.definitions import RequestBody, Response, Parameter

from diting.lrm.entrypoint import cluster_appserv
from diting.lrm.message.request import ClusterCreatingRequest, ClusterUpdatingRequest, ClusterListingRequest
from diting.lrm.message.response import ClusterResponse, ClusterListResponse

bp = Blueprint("resourcemanager", url_prefix="/rs")
logger = getLogger("diting")


@bp.post("/cluster")
@openapi.definition(
    body=RequestBody(ClusterCreatingRequest, required=True),
    summary="创建 cluster",
    tag="cluster",
    response=[Response(ClusterResponse, status=200)],
)
@validate(json=ClusterCreatingRequest)
async def create_cluster(request: Request, body: ClusterCreatingRequest) -> HTTPResponse:
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
    body = ClusterUpdatingRequest(is_alive=False)
    app_service = cluster_appserv.ClusterAppService()
    cluster_response = await app_service.update_cluster(cluster_id, body)
    if cluster_response:
        return json(cluster_response.dict())
    else:
        return json({})


@bp.post("/cluster/<cluster_id:str>")
@openapi.definition(
    body=RequestBody(ClusterUpdatingRequest, required=True),
    summary="修改 cluster",
    tag="cluster",
    response=[Response(ClusterResponse, status=200)],
)
@validate(json=ClusterUpdatingRequest)
async def update_cluster(request: Request, cluster_id: str, body: ClusterUpdatingRequest) -> HTTPResponse:
    app_service = cluster_appserv.ClusterAppService()
    cluster_response = await app_service.update_cluster(cluster_id, body)
    if cluster_response:
        return json(cluster_response.dict())
    else:
        return json({})


@bp.get("/cluster/<cluster_id:str>")
@openapi.definition(
    summary="查询单个 cluster",
    tag="cluster",
    response=[Response(ClusterResponse, status=200)],
)
async def get_cluster(request: Request, cluster_id: str) -> HTTPResponse:
    app_service = cluster_appserv.ClusterAppService()
    cluster_response = await app_service.get_cluster_by_id(cluster_id)
    if cluster_response:
        return json(cluster_response.dict())
    else:
        return json({})


@bp.get("/clusters")
@openapi.definition(
    parameter=Parameter("get_cluster_list", ClusterListingRequest, required=True),
    summary="获取多个 cluster",
    tag="cluster",
    response=[Response(ClusterListResponse, status=200)],
)
async def get_cluster_list(request: Request, parameter: ClusterListingRequest = None) -> HTTPResponse:
    if parameter is None:
        parameter = ClusterListingRequest()
    app_service = cluster_appserv.ClusterAppService()
    cluster_response = await app_service.get_cluster_list(parameter)
    if cluster_response:
        return json(cluster_response.dict())
    else:
        return json({})
