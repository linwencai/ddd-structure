from contextvars import ContextVar


# 具体实例化，参考module 相关模块
base_model_session_ctx = ContextVar("orm_session")
base_request_ctx = ContextVar("request")
