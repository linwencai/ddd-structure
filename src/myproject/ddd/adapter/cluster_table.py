import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import func
from sqlalchemy.orm import mapper
from myproject.ddd.domain import cluster_model
from myproject.ddd.adapter import Base


class Cluster(Base):
    __tablename__ = "cluster"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="id")
    name = Column(String(64), nullable=False, unique=True, comment="名称")
    desc = Column(String(256), comment="描述")
    ctime = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    mtime = Column(DateTime, default=datetime.datetime.now, onupdate=func.now(), comment="修改时间")
    is_alive = Column(Boolean, default=True, nullable=False, comment="是否有效")


def start_mappers():
    mapper(
        cluster_model.Cluster,
        Cluster,
    )
