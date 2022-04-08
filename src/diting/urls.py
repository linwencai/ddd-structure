from sanic import Blueprint

from diting.lrm.entrypoint.cluster_view import bp as cluster_bp

bp = Blueprint.group(cluster_bp, url_prefix="/lab")
