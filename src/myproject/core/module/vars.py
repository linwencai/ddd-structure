from contextvars import ContextVar

base_model_session_ctx = ContextVar("orm_session")
