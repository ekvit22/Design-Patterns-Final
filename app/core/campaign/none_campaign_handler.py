from app.core.campaign.campain_handler import CampaignHandler
from app.core.receipt import Receipt


class NoneCampaignHandler(CampaignHandler):

    def apply_campaign(self, receipt: Receipt) -> None:
        return