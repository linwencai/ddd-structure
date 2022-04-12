# import abc
# from sanic import exceptions as sanic_exception
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from diting.lrm.domain import cluster_model
# from diting.lrm.adapter import table_schema
# from diting.lrm.message.request import ClusterCreatingRequest, ClusterUpdatingRequest, ClusterListingRequest
from diting.core.ddd.base_repository import RepositoryBase
from sqlalchemy.ext.asyncio import AsyncSession
from diting.lrm.domain.cluster_model import ClusterModel

class ClusterRepository(RepositoryBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ClusterModel)
