import abc
from sqlalchemy.orm import Session
from sqlalchemy import update
from myproject.ddd.domain import cluster_model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, cluster):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, cluster_id):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, cluster):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session: Session = session

    def add(self, cluster):
        self.session.add(cluster)
        return cluster

    def get(self, cluster_id):
        return self.session.query(cluster_model.Cluster).filter_by(id=cluster_id).first()

    def update(self, cluster):
        return self.session.execute(
            update(cluster_model).where(cluster_model.id==cluster.id).values(
                name=cluster.name,
                desc=cluster.desc,
            )
        )
