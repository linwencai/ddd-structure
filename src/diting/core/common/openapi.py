import pydantic
from dataclasses import make_dataclass,field
from diting.core.common.log import app_logger as logger


def openapi_response_wrapper(model):
    name = model.__name__
    return type(
        f"Wrap{name}",
        (object,),
        {
            "code" : int,
            "msg" : str,
            "data" : model,
            "detail" : str
        }
    )