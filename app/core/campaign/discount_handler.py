from app.core.campaign.campain_handler import CampaignHandler
from app.core.receipt import Receipt


class DiscountCampaignHandler(CampaignHandler):

    def apply_campaign(self, receipt: Receipt) -> None:
        product_id, discount = self.campaign_data
        discount_percent: float = float(discount)

        for item in receipt.products:
            if item.id == product_id:
                original_price = float(item.price)
                discount_amount: float = original_price * (discount_percent / 100)
                receipt.total -= discount_amount*item.quantity
                item.total -= discount_amount*item.quantity