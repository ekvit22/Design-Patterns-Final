from app.core.campaign.campain_handler import CampaignHandler
from app.core.receipt import Receipt


class ComboCampaignHandler(CampaignHandler):

    def apply_campaign(self, receipt: Receipt) -> None:
        products, discount = self.campaign_data
        product_list = products.split('|')
        discount_amount: float = float(discount)

        if all(any(item.id == prod_id for item
                   in receipt.products) for prod_id in product_list):
            discount_amount = discount_amount/100
            for item in receipt.products:
                if item.id in product_list:
                    reduced = item.total * discount_amount
                    item.total -= reduced
                    receipt.total -= reduced