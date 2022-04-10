import logging
import sys
import socket
import os
from functools import partial
from collections import defaultdict

from sanic import Sanic
from sanic.log import access_logger, error_logger, logger

app_logger = logging.getLogger("app")

DEFAULT_LOGGING_FORMAT = (
    "[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(filename)s:%(lineno)s] "
    "%(request_info)s%(message)s"
)
DEFAULT_LOGGING_DATEFORMAT = "%Y-%m-%d %H:%M:%S %z"
old_factory = logging.getLogRecordFactory()

hostname_pid = {
    "pid" : os.getpid(),
    "hostname" : os.getpid()
}

def log_update_hostname_pid():
    global hostname_pid
    hostname_pid = {
    "pid" : os.getpid(),
    "hostname" : os.getpid()
}

class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[34m",
        "WARNING": "\033[01;33m",
        "ERROR": "\033[01;31m",
        "CRITICAL": "\033[02;47m\033[01;31m",
    }

    def format(self, record) -> str:
        prefix = self.COLORS.get(record.levelname)
        message = super().format(record)

        if prefix:
            message = f"{prefix}{message}\033[0m"

        return message

def _get_formatter(is_local, fmt, datefmt):
    formatter_type = logging.Formatter
    if is_local and sys.stdout.isatty():
        formatter_type = ColorFormatter

    return formatter_type(
        fmt=fmt,
        datefmt=datefmt,
    )

def _record_factory(*args, app, **kwargs):
    record = old_factory(*args, **kwargs)
    record.request_info = f"[{hostname_pid['hostname']}:{hostname_pid['pid']}] "

    if hasattr(app.ctx, "request"):
        request = app.ctx.request.get(None)
        if request:
            # TODO 显示 request id， 先停用
            #display = " ".join([str(request.id), request.method, request.path])
            display = " ".join([request.method, request.path])
            record.request_info += f" [{display}] "

    return record


def setup_logging(app: Sanic, setup_factory: bool = True):

    global _pid, _hostname
    _pid = os.getpid()
    _hostname = socket.gethostname()

    log_config = app.config.get("log", defaultdict(dict))

    environment = app.config.get("env", "local")
    logging_level = log_config.get(
        "level",
        logging.DEBUG if environment == "local" else logging.WARNING,
    )
    fmt = log_config.get("format", DEFAULT_LOGGING_FORMAT)
    datefmt = log_config.get("datefmt", DEFAULT_LOGGING_DATEFORMAT)
    formatter = _get_formatter(environment == "local", fmt, datefmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    for lggr in (app_logger, access_logger, logger, error_logger):
        for hndlr in lggr.handlers:
            lggr.removeHandler(hndlr)
        lggr.addHandler(handler)
        lggr.setLevel(logging_level)

    if environment == "production":
        log_path = log_config.get("output", "output.log")
        log_interval = log_config.get("interval", 1)
        log_keep = log_config.get("keep", 7)
        file_handler = logging.handlers.TimedRotatingFileHandler(log_path, "D", log_interval, log_keep)
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)

    if setup_factory:
        logging.setLogRecordFactory(partial(_record_factory, app=app))

def set_logger_level(app: Sanic, log_level):

    log_level_name = logging.getLevelName(log_level)
    for lggr in (app_logger, access_logger, logger, error_logger):
        lggr.warning(f"{lggr.name} switch log-level to {log_level_name}")
        lggr.setLevel(log_level)
    app.config.get("log")['level'] = log_level
