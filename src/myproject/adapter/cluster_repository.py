import abc
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from myproject.domain import cluster_model
from myproject.message import CreateClusterRequest, UpdateClusterRequest, ListRequest


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

    async def add(self, create_cluster_request: CreateClusterRequest):
        cluster = cluster_model.Cluster(**create_cluster_request.dict())
        async with self.session.begin():
            self.session.add(cluster)
        return cluster

    async def get(self, cluster_id) -> cluster_model.Cluster:
        # cluster = self.session.query(cluster_model.Cluster).filter_by(id=cluster_id).first()
        stmt = select(cluster_model.Cluster).filter_by(id=cluster_id)
        cluster = (await self.session.execute(stmt)).scalars().first()
        if cluster is None:
            # TODO
            pass
        return cluster

    async def update(self, cluster_id, update_cluster_request: UpdateClusterRequest):
        async with self.session.begin():
            # cluster = await self.get(cluster_id)
            # if update_cluster_request.name is not None:
            #     cluster.name = update_cluster_request.name
            # if update_cluster_request.desc is not None:
            #     cluster.desc = update_cluster_request.desc
            # if update_cluster_request.is_alive is not None:
            #     cluster.is_alive = update_cluster_request.is_alive

            # FIXME
            cluster = cluster_model.Cluster(
                name=update_cluster_request.name,
                desc=update_cluster_request.desc,
                is_alive=update_cluster_request.is_alive
            )
            cluster.id = cluster_id
            await self.session.merge(cluster)
        return cluster

    async def list(self, list_request: ListRequest):
        offset = list_request.offset * list_request.limit
        limit = list_request.limit
        # return self.session.query(cluster_model.Cluster).filter_by(is_alive=True).offset(offset).limit(limit)
        stmt = select(cluster_model.Cluster).filter_by(is_alive=True).offset(offset).limit(limit)
        return (await self.session.execute(stmt)).scalars()
