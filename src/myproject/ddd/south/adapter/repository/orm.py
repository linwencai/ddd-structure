import datetime
from email.policy import default
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy import func
from sqlalchemy.orm import mapper, relationship, declarative_base
from myproject.ddd.domain import model

Base = declarative_base()

class Cluster(Base):
    __tablename__ = "cluster"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="id")
    name = Column(String(64), nullable=False, unique=True, comment="名称")
    desc = Column(String(256), comment="描述")
    ctime = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    mtime = Column(DateTime, default=datetime.datetime.now, onupdate=func.now(), comment="修改时间")
    is_alive= Column(Boolean, default=True, nullable=False, comment="是否有效")

    def to_json(self):
        return {
            "id" : self.id,
            "name" : self.name
        }


def start_mappers():
    mapper(
        model.Cluster,
        Cluster,
    )
