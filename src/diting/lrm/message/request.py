"""
定义 前端输入的校验
"""
from typing import Optional
from diting.core.base.message import QueryRequestBase, PaginationRequestBase, DeleteRequestBase, UpdateRequestBase, CreateRequestBase

class ClusterCreatingRequest(CreateRequestBase):
    name: Optional[str]
    desc: Optional[str]
    alived: Optional[bool]
    type: Optional[str]
    cpu_value: Optional[int]
    memory_value: Optional[int]
    ingress_host: Optional[str]
    ingress_port: Optional[int]
    kube_config: Optional[str]
    harbor_url: Optional[str]
    harbor_secret: Optional[str]

class ClusterDeletingRequest(DeleteRequestBase):
    pass

class ClusterUpdatingRequest(UpdateRequestBase):
    id : str
    name: Optional[str] = ""
    desc: Optional[str] = ""
    alived: Optional[bool] = True


class ClusterGetingRequest(QueryRequestBase):
    pass

class ClusterListingRequest(PaginationRequestBase):
    pass
