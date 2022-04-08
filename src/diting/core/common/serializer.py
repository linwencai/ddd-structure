from sanic import json

def message(retval, status):
    return json(
        {
            "code" : 0,
            "msg" : "ok",
            "data" : retval,
            "detail" : {}
        },
        status=status,
    )