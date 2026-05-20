import pytest
from routes.Routes import Routes
from utils import ConfigReader
import logging
import os
import requests

from utils.ConfigReader import ReadConfig

LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "test_logging.log"))
logging.basicConfig(
   filename=LOG_FILE,
   level=logging.DEBUG,
   format="%(asctime)s | %(levelname)s | %(message)s",
   filemode='a'  # Add data to log file each run
)
logger = logging.getLogger()
# Wrapper around requests to log request & response
def log_request_response(response: requests.Response):
   req = response.request
   logger.info(f"REQUEST: {req.method} {req.url}")
   logger.info(f"Request Headers: {req.headers}")
   if req.body:
       logger.info(f"Request Body: {req.body}")
   logger.info(f"RESPONSE Status: {response.status_code}")
   logger.info(f"Response Headers: {response.headers}")
   try:
       logger.info(f"Response Body: {response.json()}")
   except Exception:
       logger.info(f"Response Body: {response.text}")


@pytest.fixture(scope="class", autouse=True)
def setup():
    # base_url = Routes.BASE_URL
    # config_reader = ReadConfig
    original_request = requests.Session.request

    def custom_request(self, method, url, **kwargs):
        response = original_request(self, method, url, **kwargs)
        log_request_response(response)
        return response

    requests.Session.request = custom_request

    yield {"base_url":Routes.BASE_URL,"config_reader":ReadConfig}