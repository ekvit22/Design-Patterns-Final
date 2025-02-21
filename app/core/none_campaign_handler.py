from app.core.campain_handler import CampaignHandler


class NoneCampaignHandler(CampaignHandler):
    def __init__(self, next_handler=None):
        super().__init__(next_handler)

    def apply_campaign(self, receipt):
        pass