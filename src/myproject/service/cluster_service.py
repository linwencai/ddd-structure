"""

"""
from myproject.core.ddd.base import DomainService
from myproject.adapter import SqlAlchemyRepository
from myproject.message import CreateClusterRequest, UpdateClusterRequest, ListRequest


class ClusterService(DomainService):

    def __init__(self):
        self.repository = SqlAlchemyRepository(self.session)
        # TODO
        # self.UOF

    async def create_cluster(self, create_cluster_request: CreateClusterRequest):
        return await self.repository.add(create_cluster_request)

    async def get_cluster_by_id(self, cluster_id: int):
        return await self.repository.get(cluster_id)

    async def update_cluster(self, cluster_id, update_cluster_request: UpdateClusterRequest):
        return await self.repository.update(cluster_id, update_cluster_request)

    async def get_cluster_list(self, list_request: ListRequest):
        return await self.repository.list(list_request)