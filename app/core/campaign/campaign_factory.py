from typing import List, Optional

from app.core.campaign.buyn_getn_handler import BuyNGetNHandler
from app.core.campaign.campaign import Campaign
from app.core.campaign.campain_handler import CampaignHandler
from app.core.campaign.combo_handler import ComboCampaignHandler
from app.core.campaign.discount_handler import DiscountCampaignHandler
from app.core.campaign.none_campaign_handler import NoneCampaignHandler


class CampaignFactory:
    @staticmethod
    def create_campaign_handler(campaign: Campaign,
                    next_handler: Optional[CampaignHandler]=None) -> CampaignHandler:
        parts = campaign.description.split(";")

        if len(parts) < 2:
            raise ValueError(f"Invalid campaign format: {campaign.description}")

        campaign_type = parts[0]

        if campaign_type == "discount":
            return DiscountCampaignHandler(campaign, next_handler)
        elif campaign_type == "combo":
            return ComboCampaignHandler(campaign, next_handler)
        elif campaign_type == "buyngetn":
            return BuyNGetNHandler(campaign, next_handler)
        else:
            raise ValueError(f"Unknown campaign type: {campaign_type}")

    @staticmethod
    def build_chain(campaigns: List[Campaign]) -> CampaignHandler:
        chain: CampaignHandler = NoneCampaignHandler(
            Campaign(id="",name="None",description="None;"))
        for campaign in campaigns:
            chain = CampaignFactory.create_campaign_handler(campaign, chain)
        return chain
