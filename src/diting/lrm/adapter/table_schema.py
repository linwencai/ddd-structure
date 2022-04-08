from email.policy import default
from xml.etree.ElementTree import Comment
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, func, Enum, Text
from diting.core.ddd.base_table import TableBase

class ClusterTable(TableBase):
    __tablename__ = "lrm_cluster"

    id = Column(String(64), primary_key=True, comment="id")
    name = Column(String(64), nullable=False, comment="名称")
    desc = Column(String(256), comment="描述")
    ctime = Column(TIMESTAMP(), index=True, server_default=text("CURRENT_TIMESTAMP"),comment="创建时间")
    mtime = Column(TIMESTAMP(), server_default=text("CURRENT_TIMESTAMP"), onupdate=func.now(), comment="修改时间")
    alived = Column(Boolean, default=True, nullable=False, comment="是否有效")

    type = Column(String(16), default="native", comment="集群类别， [native, kaiyang]")

    cpu_value = Column(Integer, default=0, comment="cpu 配额")
    cpu_unit = Column(String(8), default="m", comment="cpu 单位")
    
    memory_value = Column(Integer, default=0, comment="memory 配额")
    memory_unit = Column(String(8), default="Mi", comment="mrmory 单位")

    ingress_ip = Column(String(16), comment="ingress ip 地址")
    ingress_host = Column(String(64), comment="ingress 域名")
    ingress_port = Column(Integer, default=80, comment="ingress 端口")

    kube_config = Column(Text, default="", comment="K8S 连接串")

    harbor_address = Column(String(128), default="", comment="harbor地址")
    harbor_secret = Column(String(32), default="", comment="harbor secret")

    __table_args__ = ({'comment': '计算集群信息表'})

    # def get_columnset(self): 
    #     return set([attr for attr in dir(self) if not attr.startswith("_") and not attr in ("metadata", "registry") and not callable(getattr(self, attr))])
    
    # def from_dict(self, kwargs):
    #     columnset = self.get_columnset()
    #     for key, value in kwargs.items():
    #         if key in columnset:
    #             setattr(self, key, value)
    #     return self

    # def to_dict(self):
    #     columnset = self.get_columnset()
    #     ret = {}
    #     for key in columnset:
    #         ret[key] = getattr(self, key)
    #     return ret