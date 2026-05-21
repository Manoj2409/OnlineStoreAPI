import os

import pytest
import requests

from datamodels.Product import Product
from routes.Routes import Routes
from utils.DataProviders import read_json_data


path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "testData", "product.json"))


class TestProductDataDrivenAPI:

    @pytest.fixture(autouse=True)
    def init_class_vars(self, setup):
        self.base_url = setup["base_url"]
        self.config = setup["config_reader"]

    @pytest.mark.regression
    @pytest.mark.parametrize("product_data", read_json_data(path))
    def test_add_and_delete_product_from_json(self, product_data):
        data = product_data[0]

        payload = Product(
            data["title"],
            float(data["price"]),
            data["description"],
            data["image"],
            data["category"],
        )

        response = requests.post(self.base_url + Routes.CREATE_PRODUCT, json=payload.__dict__)
        assert response.status_code == 201

        response_data = response.json()
        assert response_data["title"] == payload.title

        product_id = response_data["id"]
        endpoint = self.base_url + Routes.DELETE_PRODUCT.format(id=product_id)

        response = requests.delete(endpoint)
        assert response.status_code == 200
