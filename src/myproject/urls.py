from sanic import Blueprint

from myproject.ddd.entrypoint.cluster_view import bp as cluster_bp

bp = Blueprint.group(cluster_bp, version=1, version_prefix="/api/v")
