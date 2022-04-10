from dataclasses import dataclass, field
from datetime import datetime
from pydoc import describe

from diting.core.ddd.base_value import Aggregation, ValueObject

@dataclass
class Quota(ValueObject):
    value : int=0
    unit : str=""

@dataclass
class Ingress(ValueObject):
    ip : str=""
    host : str=""
    port : int=80

@dataclass
class K8SAuth(ValueObject):
    config : str=""

    def __post__init(self):
        # TODO, 解密下前端传过来的内容, 基于Fernet加解密
        # self.config = XXXX
        pass


@dataclass
class HarborSetting(ValueObject):
    address : str=""
    secret : str=""

@dataclass
class Cluster(Aggregation):
    name : str = ""
    desc : str = ""
    type : str = ""
    cpu  : Quota = Quota(0, "m")
    memory : Quota = Quota(0, "Mi")
    ingress : Ingress = Ingress()
    kube : K8SAuth = K8SAuth()
    harbor : HarborSetting = HarborSetting()

