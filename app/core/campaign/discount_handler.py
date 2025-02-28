from app.core.campaign.campain_handler import CampaignHandler


class DiscountCampaignHandler(CampaignHandler):

    def apply_campaign(self, receipt):
        product_id, discount = self.campaign_data
        discount = float(discount)

        for item in receipt.products:
            if item.id == product_id:
                original_price = item.price
                discount_amount = original_price * (discount / 100)
                item.price = original_price - discount_amount
                receipt.total -= discount_amount*item.quantity
                item.total = item.price*item.quantity