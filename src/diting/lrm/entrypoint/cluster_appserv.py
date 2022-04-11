from diting.lrm.service.cluster_service import ClusterService
from diting.lrm.message.request import ClusterCreatingRequest, ClusterUpdatingRequest, ClusterListingRequest
from diting.lrm.message.response import ClusterResponse, ClusterListResponse

from diting.core.common.log import app_logger as logger


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
            return ClusterResponse.make_from_domain(cluster)
        except Exception as err:
            logger.exception("Exception:%s", err)
            return

    async def get_cluster_by_id(self, cluster_id: str):
        # get 逻辑，直接在appservice 通过仓库拿
        cluster = await self.domainservice.repository.get(cluster_id)
        return ClusterResponse.make_from_domain(cluster)

    async def update_cluster(self, cluster_id, update_cluster_request: ClusterUpdatingRequest):
        cluster = await self.domainservice.update_cluster(cluster_id, update_cluster_request)
        return ClusterResponse.make_from_domain(cluster)


    # async def get_cluster_list(self, list_request: ClusterListingRequest):
    #     try:
    #         cluster_list = await self.domainservice.get_cluster_list(list_request)
    #         return ClusterListResponse(data=[ClusterResponse.from_orm(cluster) for cluster in cluster_list])
    #     except Exception as err:
    #         app_logger.exception("Exception:%s", err)
    #         return
