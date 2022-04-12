from dataclasses import dataclass, field
from datetime import datetime

from diting.core.ddd.base_model import BusinessModelBase
@dataclass
class ClusterModel(BusinessModelBase):

    type: str = None
    cpu_value: int = None
    memory_value: int = None
    ingress_host: str = None
    ingress_port: int = None
    kube_config: str = None
    harbor_url: str = None
    harbor_secret: str = None