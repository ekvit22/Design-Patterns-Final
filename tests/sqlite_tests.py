from app.core.Repository import Repository
from app.core.campaign import Campaign
from app.infra.sqlite import Sqlite


def test_campaign_sql_memory() -> None:
    campaigns: Repository[Campaign] = Sqlite().offers()
    campaign1 = Campaign("4444","discount",product_id="1234",discount=10)
    campaign2 = Campaign("333", "combo", products=["1234","12345"], discount=10)
    campaigns.create(campaign1)
    campaigns.create(campaign2)

    res = campaigns.get_all()
    assert res[0].id == campaign1.id
    assert res[1].id == campaign2.id

    campaigns.delete(campaign1.id)

    res = campaigns.get_all()
    assert len(res) == 1
    assert res[0].id == campaign2.id

test_campaign_sql_memory()