import json
import pathlib
import inspect
from datetime import timedelta
from functools import lru_cache
from aiohttp import ClientSession
from app.utils.errors import CurrencyNotAvailableError
from app.utils.lru_cache_ttl import lru_cache_ttl

url = 'https://www.cbr-xml-daily.ru/daily_json.js'

@lru_cache_ttl(ttl_delta=timedelta(minutes=30))
async def get_currency():
    async with ClientSession() as client:
        async with client.get(url=url) as responce:
            if responce.status==200:
                return await responce.json(content_type="application/javascript", encoding="utf-8")
            else:
                raise CurrencyNotAvailableError()

# def get_currency_from_file():
#     base_dir = pathlib.Path(__file__).parent
#     with open(base_dir.joinpath("daily_json.js"), "r", encoding="utf-8") as f:
#         return json.load(f)

async def currency_list():
    currency = await get_currency()
    cur = dict()
    for key, val in currency["Valute"].items():
        cur[key]=val["Name"]
    return cur