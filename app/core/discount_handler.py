from app.core.campain_handler import CampaignHandler


class DiscountCampaignHandler(CampaignHandler):
    def __init__(self, campaign, next_handler=None):
        super().__init__(next_handler)
        self.campaign = campaign

    def apply_campaign(self, receipt):
        for item in receipt.products:
            if item.id == self.campaign.product_id:
                original_price = item.price
                discount_amount = original_price * (self.campaign.discount / 100)
                item.price = original_price - discount_amount
                print(f"Discount applied on product {item.id}: {original_price} -> {item.price}")