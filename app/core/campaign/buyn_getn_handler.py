from app.core.campaign.campain_handler import CampaignHandler
from app.core.receipt import Products, Receipt


class BuyNGetNHandler(CampaignHandler):

    def apply_campaign(self, receipt: Receipt) -> None:
        product_id, gift_id, gift_required_count = self.campaign_data
        required_count = int(gift_required_count)

        count = sum(item.quantity for item in receipt.products if item.id == product_id)
        if count >= required_count:
            receipt.products.append(Products(gift_id, 1, 0, 0))