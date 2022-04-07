from dataclasses import asdict, dataclass, is_dataclass
import pydantic
import json
import uuid
from datetime import date, datetime
from dataclasses import dataclass, field, is_dataclass
from collections import defaultdict
from typing import Optional, Union
from diting.core.common.context import base_model_session_ctx

from collections.abc import MutableMapping
from collections import defaultdict
from functools import partial

class ComplexEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-m-%d %H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def _nested(d: MutableMapping, sep_keys: list, value):
    if len(sep_keys) == 0:
        return
    
    if len(sep_keys) == 1:
        d[sep_keys[0]] = value
        return
    else:
        _nested(d[sep_keys[0]], sep_keys[1:], value)
        
def unflatten_dict(d: MutableMapping, sep: str="_") -> MutableMapping:
    infinite_defaultdict = defaultdict(partial(defaultdict, dict))
    
    for key, value in d.items():
        if key.endswith("_id"):
            # id 结尾的key， 主要是外键，不进行切分【强约束】
            sep_keys = [key]
        else:
            sep_keys = key.split(sep)
        _nested(infinite_defaultdict, sep_keys, value)
    return json.loads(json.dumps(infinite_defaultdict, cls=ComplexEncoder))

def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str ='_') -> MutableMapping:
    items = []

    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# ----------------------request---------------------------------- #
class QueryRequestBase(pydantic.BaseModel):
    cond : dict=defaultdict(str)

class PaginationRequestBase(QueryRequestBase):
    limit: int=30
    offset: int=0

# ----------------------领域服务--------------------------------- #
class DomainService:
    @property
    def session(self):
        return base_model_session_ctx.get()

# ----------------------实体、值对象、聚合------------------------------------- #
@dataclass
class ObjBase:
    @classmethod
    def make_from_dict(cls, **kwargs):
        '''
        OBJ.from_dict(**dict)
        '''
        construction_params = {}
        for key, value in kwargs.items():
            dataclass_fields = getattr(cls, "__dataclass_fields__", {})
            if key not in dataclass_fields:
                # 外部参数非dataclass field， 跳过
                continue
            
            # 获取 field 对应值的元类
            field_obj_metatype = dataclass_fields[key].type
            if is_dataclass(field_obj_metatype) and isinstance(value, MutableMapping):
                # 属于 dataclass， 且 构造值是 dict, 交给 field 自行初始化
                construction_params[key] = field_obj_metatype.make_from_dict(**value)
            else:
                # 其他情况直接进行赋值
                construction_params[key] = value
        
        return cls(**construction_params)

    @classmethod
    def make_from_flatten_dict(cls, sep="_", **kwargs):
        regular_dict = unflatten_dict(kwargs, sep=sep)
        return cls.make_from_dict(**regular_dict)

    def flatten(self):
        return flatten_dict(asdict(self), sep="_")

    def to_json(self):
        return asdict(self)

@dataclass
class Entity(ObjBase):
    id: Union[int, str]=field(default_factory=lambda : str(uuid.uuid4()))
    alived: bool=True
    ctime: datetime=field(default_factory=lambda : datetime.now())
    mtime: datetime=field(default_factory=lambda : datetime.now())

@dataclass
class ValueObject(ObjBase):
    pass

@dataclass
class Aggregation(Entity):
    pass