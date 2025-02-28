from app.core.campaign.campaign import Campaign
from app.core.campaign.campain_handler import CampaignHandler
from app.core.campaign.none_campaign_handler import NoneCampaignHandler
from constants import campaign_handlers


class CampaignFactory:
    @staticmethod
    def create_campaign_handler(campaign, next_handler=None):
        parts = campaign.description.split(";")

        if len(parts) < 2:
            raise ValueError(f"Invalid campaign format: {campaign.description}")

        campaign_type = parts[0]
        campaign_data = parts[1:]


        if campaign_type not in campaign_handlers:
            raise ValueError(f"Unknown campaign type: {campaign_type}")
        return campaign_handlers[campaign_type](campaign, next_handler)

    @staticmethod
    def build_chain(campaigns) -> CampaignHandler:
        chain = NoneCampaignHandler(Campaign(id="",name="None",description="None;"))
        for campaign in campaigns:
            chain = CampaignFactory.create_campaign_handler(campaign, chain)
        return chain
