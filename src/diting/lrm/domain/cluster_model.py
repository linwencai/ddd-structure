from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from diting.core.base.model import BusinessModelBase

@dataclass
class ClusterModel(BusinessModelBase):

    type: Optional[str] = None
    cpu_value: Optional[int] = None
    memory_value: Optional[int] = None
    ingress_host: Optional[str] = None
    ingress_port: Optional[int] = None
    kube_config: Optional[str] = None
    harbor_url: Optional[str] = None
    harbor_secret: Optional[str] = None