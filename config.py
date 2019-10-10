import json


class Config:
    def __init__(self):
        with open("config.json") as f:
            self.data = json.load(f)
            self.client_id = self.data["client_id"]
            self.client_secret = self.data["client_secret"]
            self.redis_host = self.data["redis_host"]
            self.limit = self.data["limit"]
            self.delay = self.data["delay"]
