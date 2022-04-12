from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from diting.core.ddd.base_model import ModelBase

class RepositoryBase:
    def __init__(self, session: AsyncSession, metamodel: ModelBase):
        self.session: AsyncSession = session
        self.metamodel: ModelBase = metamodel
    
    async def get(self, id:str) -> ModelBase:
        stmt = select(self.metamodel).filter_by(id=id)
        model = (await self.session.execute(stmt)).scalars().first()
        return model

    async def add(self, model: ModelBase):
        self.session.add(model)

    async def update(self, model: ModelBase, changed:dict):
        # model 对象必须是已经通过session 会话获取的对象
        for k, v in changed.items():
            if v is None:
                continue
            if not hasattr(model, k):
                continue
            setattr(model, k, v)
    
    async def delete(self, model: ModelBase):
        # model 对象必须是已经通过session 会话获取的对象
        model.alived = False
