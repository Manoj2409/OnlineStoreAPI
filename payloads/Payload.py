import random

from faker import Faker

from datamodels.Product import Product


class Payload:
    faker=Faker()
    categories=["electronics","furniture","clothing","beauty","books"]

    def product_payload(self)->Product:
        title=self.faker.unique.catch_phrase()
        price=float(self.faker.pricetag().replace("$","").replace(",",""))
        description=self.faker.sentence()
        image_url="https://i.pravatar.cc/100"
        category=random.choice(self.categories)

        return Product(title,price,description,image_url,category)


        # title: str
        # price: float
        # description: str
        # image: str
        # category: str
