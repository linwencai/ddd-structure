import abc
from myproject.ddd.south.adapter.repository import orm
from myproject.ddd.domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, cluster):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, cluster_id):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def add(self, cluster):
        self.session.add(cluster)

    def get(self, cluster_id):
        return self.session.query(model.Cluster).filter_by(id=cluster_id).first()
