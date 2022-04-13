from diting.core.base.repository import RepositoryBase
from sqlalchemy.ext.asyncio import AsyncSession
from diting.lrm.domain.cluster_model import ClusterModel

class ClusterRepository(RepositoryBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ClusterModel)
