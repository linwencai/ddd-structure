from diting.core.common.context import base_model_session_ctx
from diting.core.base.repository import RepositoryBase
from typing import Optional

class ServiceBase:

    @property
    def session(self):
        return base_model_session_ctx.get()

    def set_repository(self, repository: RepositoryBase):
        self.repository = repository