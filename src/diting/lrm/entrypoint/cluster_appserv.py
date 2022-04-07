import logging
from diting.lrm.service.cluster_service import ClusterService
from diting.lrm.message.request import ClusterCreatingRequest, ClusterUpdatingRequest, ClusterListingRequest
from diting.lrm.message.response import ClusterResponse, ClusterListResponse

app_logger = logging.getLogger("diting")


class AppService:
    _session = None

    def __init__(self, session):
        _session = session


class ClusterAppService:

    domainservice: ClusterService

    def __init__(self):
        super().__init__()
        self.domainservice = ClusterService()

    def set_service(self, service: ClusterService):
        self.domainservice = service

    async def create_cluster(self, create_cluster_request: ClusterCreatingRequest):
        try:
            cluster = await self.domainservice.create_cluster(create_cluster_request)
            return ClusterResponse.from_orm(cluster)
        except Exception as err:
            app_logger.exception("Exception:%s", err)
            return

    async def get_cluster_by_id(self, cluster_id: int):
        try:
            cluster = await self.domainservice.get_cluster_by_id(cluster_id)
            if cluster:
                return ClusterResponse.from_orm(cluster)
            else:
                return
            # return cluster
        except Exception as err:
            app_logger.exception("Exception:%s", err)
            return

    async def update_cluster(self, cluster_id, update_cluster_request: ClusterUpdatingRequest):
        try:
            cluster = await self.domainservice.update_cluster(cluster_id, update_cluster_request)
            return ClusterResponse.from_orm(cluster)
        except Exception as err:
            app_logger.exception("Exception:%s", err)
            return

    async def get_cluster_list(self, list_request: ClusterListingRequest):
        try:
            cluster_list = await self.domainservice.get_cluster_list(list_request)
            return ClusterListResponse(data=[ClusterResponse.from_orm(cluster) for cluster in cluster_list])
        except Exception as err:
            app_logger.exception("Exception:%s", err)
            return
