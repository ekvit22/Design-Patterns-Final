from app.core.campaign.buyn_getn_handler import BuyNGetNHandler
from app.core.campaign.combo_handler import ComboCampaignHandler
from app.core.campaign.discount_handler import DiscountCampaignHandler

campaign_handlers = {
    "discount": DiscountCampaignHandler,
    "combo": ComboCampaignHandler,
    "buyngetn": BuyNGetNHandler,
}