from dataclasses import dataclass


@dataclass
class Campaign:
    id: str
    name: str
    description: str

    def __init__(self, id: str, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description
