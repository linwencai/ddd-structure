"""

"""
from diting.core.ddd.base_value import DomainService
from diting.lrm.adapter.cluster_repository import ClusterRepository
from diting.lrm.message.request import ClusterCreatingRequest, ClusterUpdatingRequest, ClusterListingRequest
from diting.lrm.domain.cluster_model import ClusterModel

class ClusterService(DomainService):

    def __init__(self):
        self.repository = ClusterRepository(self.session)
        # TODO
        # self.UOF

    async def create_cluster(self, model: ClusterModel):
        return await self.repository.add(model)

    async def get_cluster_by_id(self, cluster_id: str):
        return await self.repository.get(cluster_id)

    # async def update_cluster(self, cluster_id, update_cluster_request: ClusterUpdatingRequest):

    #     changed_value = update_cluster_request.dict()
    #     changed_value.pop('id')

    #     return await self.repository.update(cluster_id, changed_value)

    # async def get_cluster_list(self, list_request: ClusterListingRequest):
    #     return await self.repository.list(list_request)