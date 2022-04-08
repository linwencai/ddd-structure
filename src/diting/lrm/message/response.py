"""
消息契约：返回给前端的内容
"""
from datetime import date, datetime
from dataclasses import dataclass, field
from typing import Any, List, Union
import pydantic
from diting.lrm.domain.cluster_model import Quota, Ingress, K8SAuth, HarborSetting
from diting.core.ddd.base_value import ResponseEntity

@dataclass
class ClusterResponse(ResponseEntity):
    name : str = ""
    desc : str = ""
    type : str = "native"
    cpu  : Quota = Quota(0, "m")
    memory : Quota = Quota(0, "Mi")
    ingress : Ingress = Ingress()
    harbor : HarborSetting = HarborSetting()

class ClusterListResponse(ResponseEntity):
    data: List[ClusterResponse]
    