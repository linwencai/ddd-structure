from sanic import Blueprint

from diting.lrm.entrypoint.cluster_view import bp as cluster_bp
from diting.lrm.entrypoint.system_view import bp as system_bp
bp = Blueprint.group([cluster_bp, system_bp], url_prefix="/lab")
