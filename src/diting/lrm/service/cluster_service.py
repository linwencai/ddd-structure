"""

"""
from diting.core.ddd.base_value import DomainService
from diting.lrm.adapter.cluster_repository import ClusterRepository
from diting.lrm.message.request import ClusterCreatingRequest, ClusterUpdatingRequest, ClusterListingRequest


class ClusterService(DomainService):

    def __init__(self):
        self.repository = ClusterRepository(self.session)
        # TODO
        # self.UOF

    async def create_cluster(self, create_cluster_request: ClusterCreatingRequest):
        return await self.repository.add(create_cluster_request)

    async def get_cluster_by_id(self, cluster_id: int):
        return await self.repository.get(cluster_id)

    async def update_cluster(self, cluster_id, update_cluster_request: ClusterUpdatingRequest):
        return await self.repository.update(cluster_id, update_cluster_request)

    async def get_cluster_list(self, list_request: ClusterListingRequest):
        return await self.repository.list(list_request)