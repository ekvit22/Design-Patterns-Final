
from pydantic import BaseModel


class CreateCampaignRequest(BaseModel):
    name: str
    description: str