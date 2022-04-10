#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Optional, Sequence, Tuple

from sanic import Sanic
from sanic.response import json
# Modules imported here should NOT have a Sanic.get_app() call in the global
# scope. Doing so will cause a circular import. Therefore, we programmatically
# import those modules inside the create_app() factory.

# from ditingcommon.csrf import setup_csrf
from diting.core.common.log import setup_logging
from diting.core.module.module import setup_modules
from diting.core.common.request_id import CustomRequest
from diting.config import APP_CONFIG, SANIC_CONFIG

APPNAME = APP_CONFIG['APP']

DEFAULT: Tuple[str, ...] = (
    "diting.core.common.context",
    "diting.core.module.orm",
    "diting.core.ddd.exception",
    "diting.core.module.redis",
    "diting.core.module.scheduler",
    "diting.core.module.snowflake",   # snowflake 必须在redis 后启动，依赖redis incr 特性
    "diting.urls",
)

# 全局注入了：
# app.ctx.redis
# app.ctx.orm_session
def create_app(module_names: Optional[Sequence[str]] = None) -> Sanic:
    """
    Application factory: responsible for gluing all of the pieces of the
    application together. In most use cases, running the application will be
    done will a None value for module_names. Therefore, we provide a default
    list. This provides flexibility when unit testing the application. The main
    purpose for this pattern is to avoid import issues. This should be the
    first thing that is called.
    """
    if module_names is None:
        module_names = DEFAULT

    app = Sanic(APPNAME, request_class=CustomRequest)
    app.config.update(APP_CONFIG)
    app.config.update(SANIC_CONFIG)
    app.config.STATIC_DIR=Path(__file__).parent / "static"

    setup_logging(app)
    setup_modules(app, *module_names)

    return app

app = create_app()

@app.get("/config")
async def get_config(request):
    from diting.core.common.log import app_logger as logger
    logger.info(APP_CONFIG)
    return json(APP_CONFIG)


if __name__ == "__main__":
    app.run(debug=True)
