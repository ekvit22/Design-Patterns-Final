from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.core.campaign.campaign import Campaign
from app.core.receipt import Receipt


class CampaignHandler(ABC):
    def __init__(self, campaign: Campaign, next_handler:Optional[CampaignHandler] = None) -> None:
        self.next_handler = next_handler
        self.campaign_type, *self.campaign_data = campaign.description.split(";")

    def handle(self, receipt: Receipt) -> None:
        self.apply_campaign(receipt)

        if self.next_handler:
            self.next_handler.handle(receipt)

    @abstractmethod
    def apply_campaign(self, receipt: Receipt) -> None:
        pass