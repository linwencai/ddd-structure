
from dataclasses import dataclass, field
from datetime import datetime
from typing import Union

from diting.core.common.snowflake import generate_snowflake_id

@dataclass
class ModelBase:
    pass

@dataclass
class BusinessModelBase(ModelBase):
    id: Union[int, str]=field(default_factory=generate_snowflake_id)
    name: str=None
    desc: str=None
    alived: bool=True
    ctime: datetime=field(default_factory=lambda : datetime.now())
    mtime: datetime=field(default_factory=lambda : datetime.now())


