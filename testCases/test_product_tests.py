from tokenize import endpats

import requests,pytest,json
from jinja2 import TemplateRuntimeError

from routes.Routes import Routes
from payloads.Payload import Payload

class TestProductAPI:

    @pytest.fixture(autouse=True) #I need to invoke this during every test case, so I'm creating the conftest and passing it through fixtures
    def init_class_vars(self,setup):
        self.base_url=setup["base_url"] #making it as class variable
        self.config=setup["config_reader"]
        self.category="electronics"
        self.payload=Payload().product_payload()

    def test_get_all_products(self):
        response=requests.get(self.base_url+Routes.GET_ALL_PRODUCTS)
        assert response.status_code==200
        data=response.json()
        #print(json.dumps(data,indent=3))
        assert len(data)>0

    def test_single_product_by_id(self):
        product_id=self.config.get_property("productId")
        endpoint=self.base_url + Routes.GET_PRODUCT_BY_ID.format(id=product_id)
        response=requests.get(endpoint)
        assert response.status_code==200
        data=response.json()
        # print(json.dumps(data,indent=3))

    def test_get_product_limits(self):
        endpoint = self.base_url + Routes.GET_PRODUCTS_WITH_LIMIT.format(limit=5)
        response = requests.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        # print(json.dumps(data, indent=3))

    def test_get_sorted_product_desc(self):
        endpoint = self.base_url + Routes.GET_PRODUCTS_SORTED.format(order="desc")
        response = requests.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        # print(json.dumps(data, indent=3))
        ids = [item['id'] for item in data]
        assert ids== sorted(ids,reverse=True)

    def test_get_sorted_product_asc(self):
        endpoint = self.base_url + Routes.GET_PRODUCTS_SORTED.format(order="asc")
        response = requests.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        # print(json.dumps(data, indent=3))
        ids = [item['id'] for item in data]
        assert ids== sorted(ids)

    def test_get_all_categories(self):
        endpoint=self.base_url+Routes.GET_ALL_CATEGORIES
        response = requests.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        # print(json.dumps(data, indent=3))

    def test_get_products_by_category(self):
        endpoint=self.base_url+Routes.GET_PRODUCTS_BY_CATEGORY.format(category=self.category)
        response = requests.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        # print(json.dumps(data, indent=3))

    def test_add_product(self):
        endpoint= self.base_url+Routes.CREATE_PRODUCT
        json=self.payload
        # print("\nSender payload : \n"+str(json))
        response=requests.post(endpoint,json.__dict__)
        data = response.json()
        assert response.status_code == 201
        assert data['title']== self.payload.__dict__["title"]

    @pytest.mark.dependency(depends=["add_product"])
    def test_update_a_product(self):
        product_id=self.config.get_property("productId")
        endpoint = self.base_url + Routes.UPDATE_PRODUCT.format(id=product_id)
        json=self.payload
        # print("\nSender payload : \n" + str(json))
        response = requests.put(endpoint, json.__dict__)
        data = response.json()
        assert response.status_code == 200
        assert data['title'] == self.payload.__dict__["title"]
        # print(str(response))

    @pytest.mark.dependency(depends=["add_product"])
    def test_delete_product(self):
        product_id = self.config.get_property("productId")
        endpoint=self.base_url+Routes.DELETE_PRODUCT.format(id=product_id)
        response=requests.delete(endpoint)
        data=response.json()
        # print(json.dumps(data,indent=4))
        assert response.status_code==200
