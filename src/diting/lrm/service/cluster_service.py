from diting.core.base.service import ServiceBase
from diting.lrm.adapter.model_repository import ClusterRepository
from diting.lrm.message.request import ClusterGetingRequest, ClusterCreatingRequest, ClusterUpdatingRequest, ClusterListingRequest
from diting.lrm.domain.cluster_model import ClusterModel
from diting.lrm.message.response import ClusterResponse

class ClusterService(ServiceBase):
    def __init__(self):
        self.cluster_repository: ClusterRepository = ClusterRepository(self.session)

    async def create_cluster(self, create_cluster_request: ClusterCreatingRequest):

        async with self.session.begin():
            cluster_model_creating = ClusterModel.from_dict(**create_cluster_request.dict())
            cluster_model_created = await self.cluster_repository.add(cluster_model_creating)

        return ClusterResponse.from_domain(cluster_model_created)

    async def get_cluster_by_id(self, id: str):
        cluster_model =  await self.cluster_repository.get(id)

        return ClusterResponse.from_domain(cluster_model)
 