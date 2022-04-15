from dataclasses import is_dataclass
from functools import wraps
from inspect import isawaitable, isclass
from typing import Optional, Union, List, Dict, Any, Sequence, Type, Callable
from pydantic import BaseModel
from sanic import Request
from sanic_ext import openapi, serializer
from sanic_ext.exceptions import InitError
from sanic_ext.extras.validation.setup import do_validation, generate_schema
from sanic_ext.extensions.openapi import definitions
from diting.core.common.serializer import message


def openapi_response_wrapper(model):
    name = model.__name__
    return type(
        f"Wrap{name}",
        (object,),
        {
            "code": int,
            "msg": str,
            "data": model,
            "detail": str
        }
    )


def _validate(
        json: Optional[Union[Callable[[Request], bool], Type[object]]] = None,
        form: Optional[Union[Callable[[Request], bool], Type[object]]] = None,
        query: Optional[Union[Callable[[Request], bool], Type[object]]] = None,
        body_argument: str = "body",
        query_argument: str = "query",
):
    schemas = {
        key: generate_schema(param)
        for key, param in (
            ("json", json),
            ("form", form),
            ("query", query),
        )
    }

    if json and form:
        raise InitError("Cannot define both a form and json route validator")

    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):

            if schemas["json"]:
                await do_validation(
                    model=json,
                    data=request.json,
                    schema=schemas["json"],
                    request=request,
                    kwargs=kwargs,
                    body_argument=body_argument,
                    allow_multiple=False,
                    allow_coerce=False,
                )
            elif schemas["form"]:
                await do_validation(
                    model=form,
                    data=request.form,
                    schema=schemas["form"],
                    request=request,
                    kwargs=kwargs,
                    body_argument=body_argument,
                    allow_multiple=True,
                    allow_coerce=False,
                )
            elif schemas["query"]:
                await do_validation(
                    model=query,
                    data=_flatten_request_args(request.args),
                    schema=schemas["query"],
                    request=request,
                    kwargs=kwargs,
                    body_argument=query_argument,
                    allow_multiple=True,
                    allow_coerce=True,
                )
            retval = f(request, *args, **kwargs)
            if isawaitable(retval):
                retval = await retval
            return retval

        return decorated_function

    return decorator


def _flatten_request_args(request_args):
    args = {}
    for k, v in request_args.items():
        args[k] = v[0]

    return args


@wraps(openapi.definition)
def definition(
        *,
        exclude: Optional[bool] = None,
        operation: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        document: Optional[Union[str, definitions.ExternalDocumentation]] = None,
        tag: Optional[
            Union[
                Union[str, definitions.Tag], Sequence[Union[str, definitions.Tag]]
            ]
        ] = None,
        deprecated: bool = False,
        body: Optional[Union[Dict[str, Any], definitions.RequestBody, Any]] = None,
        parameter: Optional[
            Union[
                Union[Dict[str, Any], definitions.Parameter, str],
                List[Union[Dict[str, Any], definitions.Parameter, str]],
                BaseModel,
            ]
        ] = None,
        response: Optional[
            Union[
                Union[Dict[str, Any], definitions.Response, Any],
                List[Union[Dict[str, Any], definitions.Response]],
            ]
        ] = None,
        secured: Optional[Dict[str, Any]] = None,
        validate: bool = False,
        body_argument: str = "body",
):
    def _inner(func):
        nonlocal parameter, body, response

        if parameter is None:
            parameter = func.__annotations__.get("query")
        if body is None:
            body = func.__annotations__.get("body")
        if response is None:
            response = func.__annotations__.get("return")

        if isclass(parameter) and issubclass(parameter, BaseModel):
            parameter = definitions.Parameter(func.__name__, parameter, required=True)

        if isclass(body) and issubclass(body, BaseModel):
            body = definitions.RequestBody(body, required=True)

        if is_dataclass(response):
            response = [definitions.Response(openapi_response_wrapper(response), status=200)]

        inner = openapi.definition(
            exclude=exclude,
            operation=operation,
            summary=summary,
            description=description,
            document=document,
            tag=tag,
            deprecated=deprecated,
            body=body,
            parameter=parameter,
            response=response,
            secured=secured,
            validate=validate,
            body_argument=body_argument,
        )

        func = serializer(message)(func)
        if isinstance(parameter, definitions.Parameter):
            query_model = parameter.fields["schema"]
            func = _validate(query=query_model)(func)

        if isinstance(body, definitions.RequestBody):
            json_model = body.fields["content"]
            func = _validate(json=json_model)(func)

        return inner(func)

    return _inner
