"""

"""
from sanic import Sanic
from myproject.core.ddd.base import DomainService
from myproject.ddd.adapter.cluster_repository import SqlAlchemyRepository
from myproject.ddd.message.request import CreateClusterRequest, UpdateClusterRequest
from myproject.ddd.adapter.cluster_table import Cluster

app = Sanic.get_app()


class ClusterService(DomainService):

    def __init__(self):
        self.repository = SqlAlchemyRepository(self.session)
        # TODO
        # self.UOF

    def create_cluster(self, create_cluster_request: CreateClusterRequest):
        cluster = Cluster(**create_cluster_request.dict())
        return self.repository.add(cluster)

    def get_cluster_by_id(self, cluster_id: int):
        return self.repository.get(cluster_id)

    def update_cluster(self, update_cluster_request: UpdateClusterRequest):
        cluster = Cluster(**update_cluster_request.dict())
        self.repository.update(cluster)
        return cluster
