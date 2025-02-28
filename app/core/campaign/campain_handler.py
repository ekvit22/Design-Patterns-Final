from abc import ABC, abstractmethod

class CampaignHandler(ABC):
    def __init__(self, campaign, next_handler=None):
        self.next_handler = next_handler
        self.campaign_type, *self.campaign_data = campaign.description.split(";")

    def handle(self, receipt):
        self.apply_campaign(receipt)

        if self.next_handler:
            self.next_handler.handle(receipt)

    @abstractmethod
    def apply_campaign(self, receipt):
        pass