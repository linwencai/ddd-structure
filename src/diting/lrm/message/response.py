"""
消息契约：返回给前端的内容
"""
from datetime import datetime
from dataclasses import dataclass
from typing import List
from diting.core.base.message import ResponseBase

@dataclass
class ClusterResponse(ResponseBase):
    id: str
    name: str
    desc: str
    alived: bool
    ctime: datetime
    mtime: datetime
    type: datetime
    cpu_value: int
    memory_value: int
    ingress_host: str
    ingress_port: int
    harbor_url: str
    harbor_secret: str

class ClusterListResponse(ResponseBase):
    data: List[ClusterResponse]
    