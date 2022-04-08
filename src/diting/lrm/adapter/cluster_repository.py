import abc
from sanic import exceptions as sanic_exception
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from diting.lrm.domain import cluster_model
from diting.lrm.adapter import table_schema
from diting.lrm.message.request import ClusterCreatingRequest, ClusterUpdatingRequest, ClusterListingRequest


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


class ClusterRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session: AsyncSession = session

    async def add(self, create_cluster_request: ClusterCreatingRequest):

        cluster = cluster_model.Cluster(**create_cluster_request.dict())
        cluster_table = table_schema.ClusterTable.from_dict(cluster.flatten())
        async with self.session.begin():
            self.session.add(cluster_table)
        return cluster

    async def get(self, cluster_id) -> cluster_model.Cluster:
        cluster_table = await self._get(cluster_id)
        return cluster_model.Cluster.make_from_flatten_dict(**cluster_table.to_dict())

    async def _get(self, cluster_id) -> table_schema.ClusterTable:
        stmt = select(table_schema.ClusterTable).filter_by(id=cluster_id)
        cluster_table = (await self.session.execute(stmt)).scalars().first()
        if cluster_table is None:
            raise sanic_exception.NotFound(f"can't find cluster of {cluster_id}")
        return cluster_table

    async def _update(self, cluster_id, changedvalues : dict):
        async with self.session.begin():
            cluster_table = await self._get(cluster_id)
            if cluster_table is None:
                raise sanic_exception.NotFound(f"can't find cluster of {cluster_id}")

            for key, value in changedvalues.items():
                setattr(cluster_table, key, value)

    async def update(self, cluster_id, changedvalues : dict):
        await self._update(cluster_id, changedvalues)
        return await self.get(cluster_id)

    # async def list(self, list_request: ClusterListingRequest):
    #     offset = list_request.offset * list_request.limit
    #     limit = list_request.limit
    #     # return self.session.query(cluster_model.Cluster).filter_by(is_alive=True).offset(offset).limit(limit)
    #     stmt = select(cluster_model.Cluster).filter_by(is_alive=True).offset(offset).limit(limit)
    #     return (await self.session.execute(stmt)).scalars()
