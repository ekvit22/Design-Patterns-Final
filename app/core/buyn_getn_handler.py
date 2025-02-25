from app.core.campain_handler import CampaignHandler
from app.core.receipt import Products


class BuyNGetNHandler(CampaignHandler):
    def __init__(self, campaign, next_handler=None):
        super().__init__(next_handler)
        self.campaign = campaign

    def apply_campaign(self, receipt):
        count = sum(item.quantity for item in receipt.products if item.id == self.campaign.product_id)
        if count >= self.campaign.gift_required_count:
            receipt.products.append(Products(self.campaign.gift_id, 1, 0, 0))