from sanic import Blueprint
from sanic import Request
from sanic_ext import openapi, serializer
from sanic_ext.extensions.openapi.definitions import RequestBody, Response, Parameter

from diting.core.common.validation import validate
from diting.core.common.log import app_logger as logger
from diting.core.common.openapi import openapi_response_wrapper as Wrap
from diting.core.common.serializer import message
from diting.lrm.service import cluster_service
from diting.lrm.message.request import ClusterCreatingRequest, ClusterUpdatingRequest, ClusterListingRequest, ClusterGetingRequest
from diting.lrm.message.response import ClusterResponse, ClusterListResponse

bp = Blueprint("resourcemanager", url_prefix="/lrm")

@bp.post("/cluster/create")  # type: ignore
@openapi.definition(
    body=RequestBody(ClusterCreatingRequest, required=True),
    summary="创建 cluster",
    tag="cluster",
    response=[Response(Wrap(ClusterResponse), status=200)]
)
@validate(json=ClusterCreatingRequest)
@serializer(message)
async def create_cluster(request: Request, body: ClusterCreatingRequest):

    service = cluster_service.ClusterService()
    return await service.create_cluster(body)




# @bp.post("/cluster/update")
# @openapi.definition(
#     body=RequestBody(ClusterUpdatingRequest, required=True),
#     summary="修改 cluster",
#     tag="cluster",
#     response=[Response(Wrap(ClusterResponse), status=200)],
# )
# @validate(json=ClusterUpdatingRequest)
# @serializer(message)
# async def update_cluster(request: Request, body: ClusterUpdatingRequest):
#     app_service = cluster_appserv.ClusterAppService()
#     cluster_id = body.id
#     cluster_response = await app_service.update_cluster(cluster_id, body)
#     if cluster_response:
#         return cluster_response.to_json()
#     else:
#         return {}


@bp.get("/cluster")  # type: ignore
@openapi.definition(
    parameter=Parameter("get_cluster", ClusterGetingRequest, required=True),
    summary="查询单个 cluster",
    tag="cluster",
    response=[Response(Wrap(ClusterResponse), status=200)],
)
@validate(query=ClusterGetingRequest)
@serializer(message)
async def get_cluster(request: Request, query: ClusterGetingRequest):
    service = cluster_service.ClusterService()

    return await service.get_cluster_by_id(query.id)



@bp.get("/cluster/list")
@openapi.definition(
    parameter=Parameter("get_cluster_list", ClusterListingRequest, required=True),
    summary="获取 cluster 列表",
    tag="cluster",
    response=[Response(Wrap(ClusterListResponse), status=200)],
)
@validate(query=ClusterListingRequest)
@serializer(message)
async def get_cluster_list(request: Request, query: ClusterListingRequest):

    service = cluster_service.ClusterService()

    return await service.get_cluster_list(limit=query.limit, offset=query.offset, filter_by=query.filter_by)
