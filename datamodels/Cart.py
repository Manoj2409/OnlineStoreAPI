from dataclasses import dataclass
from datamodels.CartProduct import CartProduct

@dataclass
class Cart:
    userId: int
    date: str
    products: list[CartProduct]
