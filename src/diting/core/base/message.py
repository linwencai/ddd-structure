import pydantic
from dataclasses import dataclass
from typing import Union, Dict
from diting.core.base.model import DataclassBase
#----------------Request Message ------------------------
class RequestBase(pydantic.BaseModel):
    pass

class QueryRequestBase(RequestBase):
    id : str

class PaginationRequestBase(RequestBase):
    page_num: int
    page_size: int

    @property
    def limit(self):
        return self.page_size

    @property
    def offset(self):
        return (self.page_num - 1) * self.page_size

    @property
    def filter_by(self):
        return {
            key:value for key, value in self.dict().items() \
            if key not in ("page_num", "page_size")
        }


class DeleteRequestBase(RequestBase):
    id : str

class UpdateRequestBase(RequestBase):
    pass

class CreateRequestBase(RequestBase):
    pass

# ------------------- Response Message ---------------
@dataclass
class ResponseBase(DataclassBase):
    pass
