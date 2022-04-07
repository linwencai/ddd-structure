"""
定义 前端输入的校验
"""
import pydantic
from typing import Optional
from diting.core.ddd.base_value import QueryRequestBase, PaginationRequestBase


class ClusterCreatingRequest(pydantic.BaseModel):
    name: str
    desc: str


class ClusterDeletingRequest(pydantic.BaseModel):
    is_alive: bool = True


class ClusterUpdatingRequest(pydantic.BaseModel):
    name: Optional[str] = ""
    desc: Optional[str] = ""
    is_alive: Optional[bool] = True


class ClusterGetingRequest(QueryRequestBase):
    pass


class ClusterListingRequest(PaginationRequestBase):
    pass
