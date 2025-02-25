from app.core.buyn_getn_handler import BuyNGetNHandler
from app.core.campaign import Campaign
from app.core.combo_handler import ComboCampaignHandler
from app.core.discount_handler import DiscountCampaignHandler
from app.core.receipt import Receipt, Products


def test_campaign_creation():
    campaign = Campaign("1234","test","discount",product_id="1234",discount=10)
    assert campaign.id == "1234"
    assert campaign.name == "test"
    assert campaign.type == "discount"
    assert campaign.product_id == "1234"
    assert campaign.discount == 10
    assert campaign.gift_id == ""
    assert campaign.gift_required_count == 0

def test_discount_campaign():
    campaign = DiscountCampaignHandler(Campaign("1234","test","discount",product_id="1234",discount=50))

    receipt = Receipt("4444","open",[Products("1234",1,30,30)],30)

    campaign.handle(receipt)

    assert receipt.total == 15
    assert receipt.products[0].total == 15

def test_combo_campaign():
    campaign = ComboCampaignHandler(Campaign("1234", "test", "combo", products=["1","2"], discount=50))

    receipt = Receipt("4444", "open", [Products("1", 2, 180, 360),Products("2",1,20,20), Products("3",1,5,5)], 385)

    campaign.handle(receipt)

    assert receipt.total == 195
    assert receipt.products[0].total == 180
    assert receipt.products[1].total == 10
    assert receipt.products[2].total == 5

def test_buy_n_get_n_campaign():
    campaign = BuyNGetNHandler(Campaign("1234", "test", "discount", product_id="1234", gift_id="5", gift_required_count=2))
    receipt = Receipt("4444", "open", [Products("1234", 2, 30, 60)], 60)
    campaign.handle(receipt)
    assert receipt.total == 60
    assert len(receipt.products) == 2
    assert receipt.products[1].id == "5"

def test_chain():
    campaign = ComboCampaignHandler(Campaign("1234", "test", "combo", products=["1", "2"], discount=50))
    campaign = DiscountCampaignHandler(Campaign("12345","test","discount",product_id="1234",discount=50),campaign)

    receipt = Receipt("4444", "open", [Products("1", 2, 180, 360), Products("2", 1, 20, 20), Products("1234", 1, 40, 40)],
                      420)

    campaign.handle(receipt)

    assert receipt.total == 210
    assert receipt.products[0].total == 180
    assert receipt.products[1].total == 10
    assert receipt.products[2].total == 20

def test_chain_with_overlap():
    campaign = ComboCampaignHandler(Campaign("1234", "test", "combo", products=["1", "2"], discount=50))
    campaign = DiscountCampaignHandler(Campaign("12345", "test", "discount", product_id="1", discount=50), campaign)

    receipt = Receipt("4444", "open",
                      [Products("1", 2, 180, 360), Products("2", 1, 20, 20)],
                      380)

    campaign.handle(receipt)

    assert receipt.total == 100
    assert receipt.products[0].total == 90
    assert receipt.products[1].total == 10