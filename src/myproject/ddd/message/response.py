"""
消息契约：返回给前端的内容
"""
from typing import Any, List
import pydantic


class BaseResponse(pydantic.BaseModel):

    class Config:
        orm_mode = True

    @classmethod
    def to_dict(cls, orm_obj: Any) -> dict:
        if orm_obj is None:
            return {}
        return cls.from_orm(orm_obj).dict()


class ClusterResponse(BaseResponse):
    id: int = 0
    name: str
    desc: str
    is_alive: bool


class ClusterListResponse(BaseResponse):
    data: List[ClusterResponse]
