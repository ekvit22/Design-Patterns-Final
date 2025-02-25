from app.core.campain_handler import CampaignHandler


class ComboCampaignHandler(CampaignHandler):
    def __init__(self, campaign, next_handler=None):
        super().__init__(next_handler)
        self.campaign = campaign

    def apply_campaign(self, receipt):
        if all(any(item.id == prod_id for item in receipt.products) for prod_id in self.campaign.products):
            discount = self.campaign.discount/100
            for item in receipt.products:
                if item.id in self.campaign.products:
                    reduced = item.total * discount
                    item.total -= reduced
                    receipt.total -= reduced