from app.core.campain_handler import CampaignHandler


class ComboCampaignHandler(CampaignHandler):
    def __init__(self, campaign, next_handler=None):
        super().__init__(next_handler)
        self.campaign = campaign

    def apply_campaign(self, receipt):
        if all(any(item.id == prod_id for item in receipt.products) for prod_id in self.campaign.products):
            print(f"Combo campaign applied for products {self.campaign.products}")
            receipt.total -= self.campaign.discount