"""
消息契约：返回给前端的内容
"""
from datetime import date, datetime
from typing import Any, List, Union
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
    id: Union[int, str]
    name: str
    desc: str
    alived: bool
    ctime: str
    mtime: str


class ClusterListResponse(BaseResponse):
    data: List[ClusterResponse]
