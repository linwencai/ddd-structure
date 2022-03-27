from sanic import Blueprint

from myproject.ddd.interfaces.controller.cluster import bp as cluster_bp

bp = Blueprint.group(cluster_bp, version=1, version_prefix="/api/v")