from app.core.campaign.buyn_getn_handler import BuyNGetNHandler
from app.core.campaign.campaign import Campaign
from app.core.campaign.campain_handler import CampaignHandler
from app.core.campaign.combo_handler import ComboCampaignHandler
from app.core.campaign.discount_handler import DiscountCampaignHandler
from app.core.receipt import Products, Receipt


def test_campaign_creation() -> None:
    campaign = Campaign("1234","test","discount;1234;10")
    assert campaign.id == "1234"
    assert campaign.name == "test"
    assert campaign.description == "discount;1234;10"

def test_discount_campaign() -> None:
    campaign = DiscountCampaignHandler(Campaign("1","test1","discount;1234;50"))

    receipt = Receipt("4444","open",[Products("1234",1,30,30)],30)

    campaign.handle(receipt)

    assert receipt.total == 15
    assert receipt.products[0].total == 15

def test_combo_campaign() -> None:
    "combo;1|2;50"
    campaign = ComboCampaignHandler(Campaign("1","test1","combo;1|2;50"))

    receipt = Receipt("4444", "open",
            [Products("1", 2, 180, 360),
             Products("2",1,20,20), Products("3",1,5,5)], 385)

    campaign.handle(receipt)

    assert receipt.total == 195
    assert receipt.products[0].total == 180
    assert receipt.products[1].total == 10
    assert receipt.products[2].total == 5

def test_buy_n_get_n_campaign() -> None:
    campaign = BuyNGetNHandler(Campaign("1234", "test", "buyngetn;1234;5;2"))
    receipt = Receipt("4444", "open", [Products("1234", 2, 30, 60)], 60)
    campaign.handle(receipt)
    assert receipt.total == 60
    assert len(receipt.products) == 2
    assert receipt.products[1].id == "5"

def test_chain() -> None:
    chain: CampaignHandler = ComboCampaignHandler(
        Campaign("1234", "test", "combo;1|2;50"))
    chain = DiscountCampaignHandler(Campaign("12345","test","discount;1234;50"),chain)

    receipt = Receipt("4444", "open",
            [Products("1", 2, 180, 360),
             Products("2", 1, 20, 20), Products("1234", 1, 40, 40)], 420)

    chain.handle(receipt)

    assert receipt.total == 210
    assert receipt.products[0].total == 180
    assert receipt.products[1].total == 10
    assert receipt.products[2].total == 20

def test_chain_with_overlap() -> None:
    campaign: CampaignHandler = ComboCampaignHandler(
        Campaign("1234", "test","combo;1|2;50"))
    campaign = DiscountCampaignHandler(Campaign("12345",
                                                "test","discount;1;50"), campaign)

    receipt = Receipt("4444", "open",
                      [Products("1", 2, 180, 360), Products("2", 1, 20, 20)],
                      380)

    campaign.handle(receipt)

    assert receipt.total == 100
    assert receipt.products[0].total == 90
    assert receipt.products[1].total == 10