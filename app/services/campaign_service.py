import uuid

from typing import List

from fastapi import HTTPException

from app.core.repository import Repository
from app.core.campaign.campaign import Campaign
from app.core.campaign.campaign_factory import CampaignFactory
from app.core.receipt import Receipt
from app.schemas.campaign import CreateCampaignRequest


class CampaignService:
    def __init__(self, repository: Repository[Campaign]):
        self.repository = repository

    def create(self, request: CreateCampaignRequest) -> Campaign:

        new_campaign = Campaign(
            id=str(uuid.uuid4()),
            name=request.name,
            description=request.description
        )
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

        chain = CampaignFactory.build_chain(campaigns)


        # first = True
        # chain: CampaignHandler = NoneCampaignHandler()
        # for campaign in reversed(campaigns):
        #     if first:
        #         first = False
        #         if campaign.type == "discount":
        #             chain = DiscountCampaignHandler(campaign)
        #         elif campaign.type == "combo":
        #             chain = ComboCampaignHandler(campaign)
        #         elif campaign.type == "buy_n_get_n":
        #             chain = BuyNGetNHandler(campaign)
        #         else:
        #             pass
        #         continue
        #
        #     if campaign.type == "discount":
        #         chain = DiscountCampaignHandler(campaign, next_handler=chain)
        #     elif campaign.type == "combo":
        #         chain = ComboCampaignHandler(campaign, next_handler=chain)
        #     elif campaign.type == "buy_n_get_n":
        #         chain = BuyNGetNHandler(campaign, next_handler=chain)
        #     else:
        #         pass

        chain.handle(receipt)
        return receipt
        