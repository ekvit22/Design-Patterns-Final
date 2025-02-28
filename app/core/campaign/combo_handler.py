from app.core.campaign.campain_handler import CampaignHandler


class ComboCampaignHandler(CampaignHandler):

    def apply_campaign(self, receipt):
        products, discount = self.campaign_data
        product_list = products.split('|')
        discount = float(discount)

        if all(any(item.id == prod_id for item in receipt.products) for prod_id in product_list):
            discount = discount/100
            for item in receipt.products:
                if item.id in product_list:
                    reduced = item.total * discount
                    item.total -= reduced
                    receipt.total -= reduced