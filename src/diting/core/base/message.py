import pydantic
from dataclasses import dataclass
from typing import Union
from diting.core.base.model import DataclassBase
#----------------Request Message ------------------------
class RequestBase(pydantic.BaseModel):
    pass

class QueryRequestBase(RequestBase):
    id : str

class PaginationRequestBase(RequestBase):
    page_num: int
    page_size: int

class DeleteRequestBase(RequestBase):
    id : Union[str, int]

class UpdateRequestBase(RequestBase):
    pass

class CreateRequestBase(RequestBase):
    pass

# ------------------- Response Message ---------------
@dataclass
class ResponseBase(DataclassBase):
    pass
