import logging
from myproject.service import ClusterService
from myproject.message import CreateClusterRequest, UpdateClusterRequest, ListRequest
from myproject.message import ClusterResponse, ClusterListResponse

app_logger = logging.getLogger("myproject")


class AppService:
    _session = None

    def __init__(self, session):
        _session = session


class ClusterAppService:

    _service: ClusterService

    def __init__(self):
        super().__init__()
        self._service = ClusterService()

    def set_service(self, service: ClusterService):
        self._service = service

    async def create_cluster(self, create_cluster_request: CreateClusterRequest):
        try:
            cluster = await self._service.create_cluster(create_cluster_request)
            return ClusterResponse.from_orm(cluster)
        except Exception as err:
            app_logger.exception("Exception:%s", err)
            return

    async def get_cluster_by_id(self, cluster_id: int):
        try:
            cluster = await self._service.get_cluster_by_id(cluster_id)
            if cluster:
                return ClusterResponse.from_orm(cluster)
            else:
                return
            # return cluster
        except Exception as err:
            app_logger.exception("Exception:%s", err)
            return

    async def update_cluster(self, cluster_id, update_cluster_request: UpdateClusterRequest):
        try:
            cluster = await self._service.update_cluster(cluster_id, update_cluster_request)
            return ClusterResponse.from_orm(cluster)
        except Exception as err:
            app_logger.exception("Exception:%s", err)
            return

    async def get_cluster_list(self, list_request: ListRequest):
        try:
            cluster_list = await self._service.get_cluster_list(list_request)
            return ClusterListResponse(data=[ClusterResponse.from_orm(cluster) for cluster in cluster_list])
        except Exception as err:
            app_logger.exception("Exception:%s", err)
            return
