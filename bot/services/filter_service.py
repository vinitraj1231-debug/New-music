import asyncio
from bot.core.call import call_py
from bot.database.db import db

class FilterService:
    def __init__(self):
        self.filters = {
            "bassboost": "bass=g=10,firequalizer=gain_entry='entry(0,10);entry(250,5);entry(1000,0);entry(4000,0);entry(16000,0)'",
            "nightcore": "asetrate=48000*1.25,atempo=1.25",
            "slowed": "asetrate=48000*0.8,atempo=0.8",
            "deep": "asetrate=48000*0.5,atempo=0.5",
            "reverb": "aecho=0.8:0.88:60:0.4",
            "8d": "apulsator=hz=0.125"
        }

    async def get_filter(self, name):
        return self.filters.get(name)

filter_service = FilterService()
