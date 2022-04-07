from typing import Any

from sanic import Request

from diting.core.common.trace import generate

class CustomRequest(Request):
    @classmethod
    def generate_id(*_: Any) -> str:
        return generate()