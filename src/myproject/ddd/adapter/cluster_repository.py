import abc
from sqlalchemy.orm import Session
from myproject.ddd.domain import cluster_model
from myproject.ddd.message.request import CreateClusterRequest, UpdateClusterRequest, ListRequest


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, cluster):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, cluster_id):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, cluster_id, cluster):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session: Session = session

    def add(self, create_cluster_request: CreateClusterRequest):
        cluster = cluster_model.Cluster(**create_cluster_request.dict())
        with self.session.begin():
            self.session.add(cluster)
        return cluster

    def get(self, cluster_id) -> cluster_model.Cluster:
        cluster = self.session.query(cluster_model.Cluster).filter_by(id=cluster_id).first()
        if cluster is None:
            # TODO
            pass
        return cluster

    def update(self, cluster_id, update_cluster_request: UpdateClusterRequest):
        with self.session.begin():
            cluster = self.get(cluster_id)
            if update_cluster_request.name is not None:
                cluster.name = update_cluster_request.name
            if update_cluster_request.desc is not None:
                cluster.desc = update_cluster_request.desc
            if update_cluster_request.is_alive is not None:
                cluster.is_alive = update_cluster_request.is_alive
        return cluster

    def list(self, list_request: ListRequest):
        offset = list_request.offset * list_request.limit
        limit = list_request.limit
        return self.session.query(cluster_model.Cluster).filter_by(is_alive=True).offset(offset).limit(limit)
