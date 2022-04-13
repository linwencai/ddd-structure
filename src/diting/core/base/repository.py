from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from diting.core.base.model import ModelBase
from typing import Optional

class RepositoryBase:
    def __init__(self, session: AsyncSession, metamodel: Optional[ModelBase]=None):
        self.session: AsyncSession = session
        self.metamodel: Optional[ModelBase] = metamodel
    
    def set_metamodel(self, metamodel: ModelBase):
        self.metamodel = metamodel

    async def get(self, id:str) -> ModelBase:
        stmt = select(self.metamodel).filter_by(id=id)
        model = (await self.session.execute(stmt)).scalars().first()
        return model

    async def add(self, model: ModelBase) -> ModelBase:
        self.session.add(model)
        return model

    async def update(self, model: ModelBase, changed:dict={}) -> ModelBase:
        # model 对象必须是已经通过session 会话获取的对象
        for k, v in changed.items():
            if v is None:
                continue
            if not hasattr(model, k):
                continue

            if k in ("id", "ctime", "mtime"):
                # id， ctime, mtime 不得修改
                continue

            setattr(model, k, v)
        return model
    
    async def delete(self, model: ModelBase) -> ModelBase:
        # model 对象必须是已经通过session 会话获取的对象
        setattr(model, "alived", False)
        return model
