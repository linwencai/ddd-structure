"""
定义 前端输入的校验
"""
import pydantic
from typing import Optional
from diting.core.ddd.base_value import QueryRequestBase, PaginationRequestBase
from diting.lrm.domain.cluster_model import Quota, Ingress, K8SAuth, HarborSetting


class ClusterCreatingRequest(pydantic.BaseModel):
    name: str
    desc: str
    type : str = "native"
    cpu  : Quota = Quota(0, "m")
    memory : Quota = Quota(0, "Mi")
    ingress : Ingress = Ingress()
    kube : K8SAuth = K8SAuth()
    harbor : HarborSetting = HarborSetting()


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
