from app.core.Repository import Repository
from app.core.campaign.campaign import Campaign
from app.infra.sqlite import Sqlite


def test_campaign_sql_memory() -> None:
    campaigns: Repository[Campaign] = Sqlite().campaigns()
    campaign1 = Campaign("4444","test1","discount;1234;10")
    campaign2 = Campaign("333", "test2", "combo;1234|12345;10")
    campaigns.create(campaign1)
    campaigns.create(campaign2)

    res = campaigns.get_all()
    assert len(res) == 2
    assert res[0].id == campaign1.id
    assert res[1].id == campaign2.id

    campaigns.delete(campaign1.id)

    res = campaigns.get_all()
    assert len(res) == 1
    assert res[0].id == campaign2.id