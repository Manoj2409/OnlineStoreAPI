import pytest
from routes.Routes import Routes
from utils import ConfigReader

@pytest.fixture(scope="class")
def setup():
    # base_url=Routes.BASE_URL
    # config_reader=ConfigReader.ReadConfig
    yield{"base_url":Routes.BASE_URL,"config_reader":ConfigReader.ReadConfig}
    # re-writing this into dict format