import logging
import pytest
from sanic import Sanic
from sanic.log import access_logger, logger
import __init  # Change the current working directory
from diting import server
from diting.core.common.log import app_logger
from diting.lrm.message.response import ClusterResponse


@pytest.fixture(scope="session")
def app() -> Sanic:
    access_logger.setLevel(logging.ERROR)
    logger.setLevel(logging.ERROR)
    app_logger.setLevel(logging.ERROR)
    server.app.config["access_log"] = False
    return server.app


@pytest.fixture(scope="session")
def create_cluster(app) -> ClusterResponse:
    data = {
        "name": "string",
        "desc": "string",
        "type": "string",
        "cpu_value": 0,
        "memory_value": 0,
        "ingress_host": "string",
        "ingress_port": 0,
        "kube_config": "string",
        "harbor_url": "string",
        "harbor_secret": "string"
    }
    request, response = app.test_client.post("/lab/lrm/cluster/create", json=data)

    assert request.method.lower() == "post"
    assert response.json.get("code") == 0, response.json
    assert response.status == 200

    cluster = ClusterResponse(**response.json.get("data"))
    yield cluster

    # TODO delete cluster

    return


def test_get_cluster_list(app):
    request, response = app.test_client.get("/lab/lrm/cluster/list?page_num=0&page_size=10")

    assert request.method.lower() == "get"
    assert response.json.get("code") == 0
    assert response.status == 200


def test_get_cluster(app, create_cluster: ClusterResponse):
    request, response = app.test_client.get("/lab/lrm/cluster", params={"id": create_cluster.id})

    assert request.method.lower() == "get"
    assert response.json.get("code") == 0
    assert response.status == 200
