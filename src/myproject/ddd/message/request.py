"""
定义 前端输入的校验
"""
import pydantic


class CreateClusterRequest(pydantic.BaseModel):
    name: str
    desc: str


class UpdateClusterRequest(pydantic.BaseModel):
    id: int
    name: str
    desc: str
