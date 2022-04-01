from dataclasses import dataclass
import datetime


@dataclass
class Cluster:
    id: int
    name: str
    desc: str
    ctime: datetime.datetime
    mtime: datetime.datetime
    is_alive: bool = True
