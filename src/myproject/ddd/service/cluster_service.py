"""

"""
from myproject.core.ddd.base import DomainService
from myproject.ddd.adapter.cluster_repository import SqlAlchemyRepository
from myproject.ddd.message.request import CreateClusterRequest, UpdateClusterRequest, ListRequest


class ClusterService(DomainService):

    def __init__(self):
        self.repository = SqlAlchemyRepository(self.session)
        # TODO
        # self.UOF

    def create_cluster(self, create_cluster_request: CreateClusterRequest):
        return self.repository.add(create_cluster_request)

    def get_cluster_by_id(self, cluster_id: int):
        return self.repository.get(cluster_id)

    def update_cluster(self, cluster_id, update_cluster_request: UpdateClusterRequest):
        return self.repository.update(cluster_id, update_cluster_request)

    def get_cluster_list(self, list_request: ListRequest):
        return self.repository.list(list_request)