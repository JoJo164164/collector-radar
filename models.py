from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    title: str
    price: Optional[str]
    url: str
    image: Optional[str]
    source: str
