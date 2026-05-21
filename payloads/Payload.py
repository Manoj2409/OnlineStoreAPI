import random
from datetime import datetime

from faker import Faker

from datamodels.Address import Address
from datamodels.Cart import Cart
from datamodels.CartProduct import CartProduct
from datamodels.Geolocation import Geolocation
from datamodels.Name import Name
from datamodels.Product import Product
from datamodels.User import User


class Payload:
    faker = Faker()
    categories = ["electronics", "furniture", "clothing", "beauty", "books"]

    def product_payload(self) -> Product:
        title = self.faker.unique.catch_phrase()
        price = float(self.faker.pricetag().replace("$", "").replace(",", ""))
        description = self.faker.sentence()
        image_url = "https://i.pravatar.cc/100"
        category = random.choice(self.categories)

        return Product(title, price, description, image_url, category)

    def user_payload(self) -> User:
        name = Name(
            firstname=self.faker.first_name(),
            lastname=self.faker.last_name(),
        )
        geolocation = Geolocation(
            lat=str(self.faker.latitude()),
            lng=str(self.faker.longitude()),
        )
        address = Address(
            city=self.faker.city(),
            street=self.faker.street_name(),
            number=random.randint(1, 100),
            zipcode=self.faker.zipcode(),
            geolocation=geolocation,
        )

        return User(
            email=self.faker.email(),
            username=self.faker.user_name(),
            password=self.faker.password(),
            name=name,
            address=address,
            phone=self.faker.phone_number(),
        )

    def cart_payload(self, user_id: int) -> Cart:
        product_id = random.randint(1, 100)
        quantity = random.randint(1, 10)
        cart_product = CartProduct(productId=product_id, quantity=quantity)
        today = datetime.today().strftime("%Y-%m-%d")

        return Cart(userId=int(user_id), date=today, products=[cart_product])
