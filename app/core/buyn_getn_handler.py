from app.core.campain_handler import CampaignHandler


class BuyNGetNHandler(CampaignHandler):
    def __init__(self, campaign, next_handler=None):
        super().__init__(next_handler)
        self.campaign = campaign

    def apply_campaign(self, receipt):
        count = sum(1 for item in receipt.products if item.id == self.campaign.product_id)
        if count >= self.campaign.gift_required_count:
            receipt.add_item(self.campaign.gift_id, free=True)
            print(f"Buy {self.campaign.gift_required_count} gift applied for product {self.campaign.product_id}")