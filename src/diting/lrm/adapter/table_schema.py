from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, func
from diting.core.ddd.base_table import TableBase

# from sqlalchemy.orm import declarative_base

# ----------------------ORM------------------------------------- #
# Base = declarative_base()

class ClusterTable(TableBase):
    __tablename__ = "lrm_cluster"

    id = Column(String(64), primary_key=True, comment="id")
    name = Column(String(64), nullable=False, comment="名称")
    desc = Column(String(256), comment="描述")
    ctime = Column(TIMESTAMP(), index=True, server_default=text("CURRENT_TIMESTAMP"),comment="创建时间")
    mtime = Column(TIMESTAMP(), server_default=text("CURRENT_TIMESTAMP"), onupdate=func.now(), comment="修改时间")
    alived = Column(Boolean, default=True, nullable=False, comment="是否有效")

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