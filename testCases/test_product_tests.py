import pytest
import requests

from routes.Routes import Routes
from payloads.Payload import Payload


class TestProductAPI:

    @pytest.fixture(autouse=True)
    def init_class_vars(self, setup):
        self.base_url = setup["base_url"]
        self.config = setup["config_reader"]
        self.category = "jewelery"
        self.payload = Payload().product_payload()

    @pytest.mark.smoke
    @pytest.mark.run(order=1)
    def test_get_all_products(self):
        response = requests.get(self.base_url + Routes.GET_ALL_PRODUCTS)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0

    @pytest.mark.sanity
    @pytest.mark.run(order=2)
    def test_get_single_product_by_id(self):
        product_id = self.config.get_property("productId")
        endpoint = self.base_url + Routes.GET_PRODUCT_BY_ID.format(id=product_id)
        response = requests.get(endpoint)
        assert response.status_code == 200

    @pytest.mark.regression
    @pytest.mark.run(order=3)
    def test_get_limited_products(self):
        endpoint = self.base_url + Routes.GET_PRODUCTS_WITH_LIMIT.format(limit=10)
        response = requests.get(endpoint)
        assert response.status_code == 200

    @pytest.mark.smoke
    @pytest.mark.run(order=4)
    def test_get_sorted_products_desc(self):
        endpoint = self.base_url + Routes.GET_PRODUCTS_SORTED.format(order="desc")
        response = requests.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        ids = [item['id'] for item in data]
        assert ids == sorted(ids, reverse=True)

    @pytest.mark.sanity
    @pytest.mark.run(order=5)
    def test_get_sorted_products_asc(self):
        endpoint = self.base_url + Routes.GET_PRODUCTS_SORTED.format(order="asc")
        response = requests.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        ids = [item['id'] for item in data]
        assert ids == sorted(ids)

    @pytest.mark.regression
    @pytest.mark.run(order=6)
    def test_get_all_products_all_categories(self):
        endpoint = self.base_url + Routes.GET_ALL_CATEGORIES
        response = requests.get(endpoint)
        assert response.status_code == 200

    @pytest.mark.smoke
    @pytest.mark.run(order=7)
    def test_get_products_by_categories(self):
        endpoint = self.base_url + Routes.GET_PRODUCTS_BY_CATEGORY.format(category=self.category)
        response = requests.get(endpoint)
        assert response.status_code == 200

    @pytest.mark.regression
    @pytest.mark.run(order=8)
    @pytest.mark.dependency(name="add_product")
    def test_add_new_product(self):
        response = requests.post(self.base_url + Routes.CREATE_PRODUCT, json=self.payload.__dict__)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == self.payload.title

    @pytest.mark.regression
    @pytest.mark.run(order=9)
    @pytest.mark.dependency(depends=["add_product"])
    def test_update_product(self):
        product_id = self.config.get_property("productId")
        endpoint = self.base_url + Routes.UPDATE_PRODUCT.format(id=product_id)
        response = requests.put(endpoint, json=self.payload.__dict__)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == self.payload.title

    @pytest.mark.regression
    @pytest.mark.run(order=10)
    @pytest.mark.dependency(depends=["add_product"])
    def test_delete_product(self):
        product_id = self.config.get_property("productId")
        endpoint = self.base_url + Routes.DELETE_PRODUCT.format(id=product_id)
        response = requests.delete(endpoint)
        assert response.status_code == 200
