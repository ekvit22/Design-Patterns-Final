import uuid
from http.client import HTTPException
from typing import List

from app.core.Repository import Repository
from app.core.buyn_getn_handler import BuyNGetNHandler
from app.core.campaign import Campaign
from app.core.campain_handler import CampaignHandler
from app.core.combo_handler import ComboCampaignHandler
from app.core.discount_handler import DiscountCampaignHandler
from app.core.none_campaign_handler import NoneCampaignHandler
from app.core.receipt import Receipt
from app.schemas.campaign import CreateCampaignRequest


class CampaignService:
    def __init__(self, repository: Repository[Campaign]):
        self.repository = repository

    def create(self, request: CreateCampaignRequest) -> Campaign:
        existing_campaign = self.repository.read_with_name(request.name)
        if existing_campaign is not None:
            raise HTTPException(
                status_code=409,
                detail={"message": f"Campaign with name<{request.name}> already exists."}
            )
        new_campaign = Campaign(id=str(uuid.uuid4()), name=request.name, type=request.type, product_id=request.product_id, products=request.products, discount=request.discount, gift_id=request.gift_id, gift_required_count=request.gift_required_count)

        self.repository.create(new_campaign)
        return new_campaign

    def delete(self, campaign_id: str):
        result = self.repository.read(campaign_id)
        if result is None:
            raise HTTPException(
                status_code=404,
                detail={"error": {"message": f"Campaign with id<{campaign_id}> does not exist."}}
            )
        self.repository.delete(campaign_id)

    def read_campaigns(self) -> List[Campaign]:
        return self.repository.get_all()

    def apply_campaigns(self, receipt: Receipt) -> Receipt:
        campaigns = self.repository.get_all()

        if not campaigns:
            return receipt

        chain: CampaignHandler = NoneCampaignHandler()
        for campaign in reversed(campaigns):
            if campaign.type == "discount":
                chain = DiscountCampaignHandler(campaign, next_handler=chain)
            elif campaign.type == "combo":
                chain = ComboCampaignHandler(campaign, next_handler=chain)
            elif campaign.type == "buy_n_get_n":
                chain = BuyNGetNHandler(campaign, next_handler=chain)
            else:
                pass

        chain.handle(receipt)
        return receipt
        