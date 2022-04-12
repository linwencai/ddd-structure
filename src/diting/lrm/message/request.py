"""
定义 前端输入的校验
"""
import pydantic
from typing import Optional
from diting.core.ddd.base_value import QueryRequestBase, PaginationRequestBase
class ClusterCreatingRequest(pydantic.BaseModel):

    name: str
    desc: str
    alived: bool
    type: str
    cpu_value: int
    memory_value: int
    ingress_host: str
    ingress_port: int
    kube_config: str = None
    harbor_url: str
    harbor_secret: str

class ClusterDeletingRequest(pydantic.BaseModel):
    is_alive: bool = True


class ClusterUpdatingRequest(pydantic.BaseModel):
    id : str
    name: Optional[str] = ""
    desc: Optional[str] = ""
    alived: Optional[bool] = True


class ClusterGetingRequest(QueryRequestBase):
    id : str

class ClusterListingRequest(PaginationRequestBase):
    pass
