from myproject.core.module.vars import base_model_session_ctx


class DomainService:

    # def __init__(self):
    #     self.session = base_model_session_ctx.get()
    @property
    def session(self):
        return base_model_session_ctx.get()
