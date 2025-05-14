import json
import pathlib
from aiohttp import ClientSession
from app.utils.errors import CurrencyNotAvailableError

url = 'https://www.cbr-xml-daily.ru/daily_json.js'

async def get_currency():
    async with ClientSession() as client:
        async with client.get(url=url) as responce:
            if responce.status==200:
                return await responce.json()
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