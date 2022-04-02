from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Cluster:
    id: int = field(init=False)
    name: str
    desc: str
    ctime: int = field(init=False)
    mtime: int = field(init=False)
    is_alive: bool = True
