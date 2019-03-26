"""
test_api_endpoints.py

Tests for functionality to list the available API endpoints of a remote
MyTardis server
"""
import json
import requests_mock

from mtclient.conf import config
from mtclient.models.api import ApiEndpoint

config.url = "https://mytardis-test.example.com"
config.cache_backend = "dogpile.cache.null"


def test_api_list():
    """
    Test listing the API endpoints of a remote MyTardis server
    """
    mock_api_endpoints = {
        "dataset": {
            "list_endpoint": "/api/v1/dataset/",
            "schema": "/api/v1/dataset/schema/"
        },
        "dataset_file": {
            "list_endpoint": "/api/v1/dataset_file/",
            "schema": "/api/v1/dataset_file/schema/"
        },
        "experiment": {
            "list_endpoint": "/api/v1/experiment/",
            "schema": "/api/v1/experiment/schema/"
        }
    }
    mock_api_list_response = json.dumps(mock_api_endpoints)
    with requests_mock.Mocker() as mocker:
        list_api_endpoints_url = "%s/api/v1/?format=json" % config.url
        mocker.get(list_api_endpoints_url, text=mock_api_list_response)
        endpoints = ApiEndpoint.list()
        returned_endpoints = \
            {endpoint.model: endpoint.response_dict for endpoint in endpoints}
        assert returned_endpoints == mock_api_endpoints