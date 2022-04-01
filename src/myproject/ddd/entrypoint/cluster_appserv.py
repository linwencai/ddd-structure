import logging
from myproject.ddd.domain.cluster_model import Cluster
from myproject.ddd.service.cluster_service import ClusterService
from myproject.ddd.message.request import CreateClusterRequest, UpdateClusterRequest
from myproject.ddd.message.response import ClusterResponse

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

    def create_cluster(self, create_cluster_request: CreateClusterRequest):
        try:
            cluster = self._service.create_cluster(create_cluster_request)
            return ClusterResponse.from_orm(cluster)
        except Exception as err:
            app_logger.exception("Exception:%s", err)
            return

    def get_cluster_by_id(self, cluster_id: int):
        try:
            cluster: Cluster = self._service.get_cluster_by_id(cluster_id)
            if cluster:
                return ClusterResponse.from_orm(cluster)
            else:
                return
            # return cluster
        except Exception as err:
            app_logger.exception("Exception:%s", err)
            return

    def update_cluster(self, update_cluster_request: UpdateClusterRequest):
        try:
            cluster = self._service.update_cluster(update_cluster_request)
            return ClusterResponse.from_orm(cluster)
        except Exception as err:
            app_logger.exception("Exception:%s", err)
            return
