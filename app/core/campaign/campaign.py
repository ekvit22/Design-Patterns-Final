from dataclasses import dataclass
from typing import Optional


@dataclass
class Campaign:
    id: str
    name: str
    description: str

    def __init__(self, id: str, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description
