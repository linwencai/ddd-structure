from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, func, Text, Table
from diting.core.base.table import metadata_obj


cluster_table = Table(
    "cluster",
    metadata_obj,
    Column("id", String(64), primary_key=True, comment="id"),
    Column("name", String(64), nullable=False, comment="名称"),
    Column("desc", String(256), comment="描述"),
    Column("ctime", TIMESTAMP(), index=True, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"),
    Column("mtime", TIMESTAMP(), server_default=text("CURRENT_TIMESTAMP"), onupdate=func.now(), comment="修改时间"),
    Column("alived", Boolean, default=True, nullable=False, comment="是否有效"),
    Column("type", String(16), default="native", comment="集群类别， [native, kaiyang]"),
    Column("cpu_value", Integer, default=0, comment="cpu 配额"),
    Column("memory_value", Integer, default=0, comment="memory 配额"),
    Column("ingress_host", String(128), default="", comment="ingress 域名"),
    Column("ingress_port", Integer, default=80, comment="ingress 端口"),
    Column("kube_config", Text, default="", comment="K8S 连接串"),
    Column("harbor_url", String(128), default="", comment="harbor url"),
    Column("harbor_secret", String(64), default="", comment="harbor secret")
)