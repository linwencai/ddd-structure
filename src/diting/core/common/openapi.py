
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