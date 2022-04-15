from diting.core.base.service import ServiceBase
from diting.lrm.adapter.model_repository import ClusterRepository
from diting.lrm.message.request import ClusterGetingRequest, ClusterCreatingRequest, ClusterUpdatingRequest, ClusterListingRequest
from diting.lrm.domain.cluster_model import ClusterModel
from diting.lrm.message.response import ClusterResponse, ClusterListResponse
from sanic import exceptions

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

        if cluster_model is None:
            raise exceptions.NotFound(f"cluster {id} not found")

        return ClusterResponse.from_domain(cluster_model)

    async def get_cluster_list(self, limit: int, offset: int, filter_by: dict):

        cluster_model_list = await self.cluster_repository.list(limit, offset, filter_by)

        if not cluster_model_list:
            raise exceptions.NotFound("clusters not found")
        
        return ClusterListResponse([ClusterResponse.from_domain(cluster_model) for cluster_model in cluster_model_list])

 