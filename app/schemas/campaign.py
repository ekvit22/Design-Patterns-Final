from typing import Optional, List

from pydantic import BaseModel

class CreateCampaignRequest(BaseModel):
    type: str  #"discount", "buy_n_get_n", "combo"
    name: str
    product_id: Optional[str] = ""
    products: Optional[List[str]] = []
    discount: Optional[int] = 0
    gift_id: Optional[str] = ""
    gift_required_count: Optional[int] = 0