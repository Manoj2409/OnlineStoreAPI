from dataclasses import dataclass

from datamodels.Geolocation import Geolocation


@dataclass
class Address:
    city: str
    street: str
    number: int
    zipcode: str
    geolocation: Geolocation
