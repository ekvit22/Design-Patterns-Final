from app.core.receipt import Products, Receipt
from app.infra.in_memory import InMemory
from app.schemas.campaign import CreateCampaignRequest
from app.services.campaign_service import CampaignService


def test_campaign_service() -> None:
    repository = InMemory()
    campaign_service = CampaignService(repository.campaigns())

    assert campaign_service.read_campaigns() == []

    campaign_service.create(
        CreateCampaignRequest(
            name="test",
            description="discount;1;50")
    )
    read_campaign = campaign_service.read_campaigns()[0]
    assert read_campaign.name == "test"

    receipt = Receipt("4444", "open", [Products("1", 1, 30, 30)], 30)

    campaign_service.apply_campaigns(receipt)

    assert receipt.total == 15

    campaign_service.delete(read_campaign.id)
    assert campaign_service.read_campaigns() == []