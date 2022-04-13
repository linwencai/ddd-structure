import abc
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from typing import Union, Optional

from diting.core.common.snowflake import id_generator

class DatetimeJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

@dataclass
class DataclassBase:
    @classmethod
    def from_dict(cls, **kwargs):
        '''
        从 dict 构建 dataclass, 
        OBJ.from_dict(**dict)
        '''
        construction_params = {}
        for key, value in kwargs.items():
            dataclass_fields = getattr(cls, "__dataclass_fields__", {})
            if key not in dataclass_fields:
                # 外部参数非dataclass field， 跳过
                continue
            
            construction_params[key] = value
        
        return cls(**construction_params)

    @classmethod
    def from_domain(cls, model):
        return cls.from_dict(**asdict(model))

    def to_json(self):
        return json.loads(
            json.dumps(asdict(self), cls=DatetimeJSONEncoder)
        )

@dataclass
class ModelBase(DataclassBase):
    pass

@dataclass
class BusinessModelBase(ModelBase):
    id: Union[int, str]=field(default_factory=id_generator)
    name: Optional[str]=None
    desc: Optional[str]=None
    alived: bool=True
    ctime: datetime=field(default_factory=lambda : datetime.now())
    mtime: datetime=field(default_factory=lambda : datetime.now())


