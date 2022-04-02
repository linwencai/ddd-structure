"""
定义 前端输入的校验
"""
import pydantic
from typing import Optional


class CreateClusterRequest(pydantic.BaseModel):
    name: str
    desc: str


class DeleteClusterRequest(pydantic.BaseModel):
    is_alive: bool = True


class UpdateClusterRequest(pydantic.BaseModel):
    name: Optional[str] = ""
    desc: Optional[str] = ""
    is_alive: Optional[bool] = True


class ListRequest(pydantic.BaseModel):
    limit: int = 10
    offset: int = 0
