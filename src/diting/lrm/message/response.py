"""
消息契约：返回给前端的内容
"""
from datetime import date, datetime
from dataclasses import dataclass, field
from typing import Any, List, Union
import pydantic
from diting.core.ddd.base_value import ResponseEntity

@dataclass
class ClusterResponse(ResponseEntity):
    id: str
    name: str
    desc: str
    alived: bool
    ctime: str
    mtime: str
    type: str
    cpu_value: int
    memory_value: int
    ingress_host: str
    ingress_port: int
    harbor_url: str
    harbor_secret: str

class ClusterListResponse(ResponseEntity):
    data: List[ClusterResponse]
    