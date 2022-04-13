from sanic import json
from diting.core.base.message import ResponseBase

def message(retval: ResponseBase, status):
    return json(
        {
            "code" : 0,
            "msg" : "ok",
            "data" : retval.to_json(),
            "detail" : {}
        },
        status=status
    )