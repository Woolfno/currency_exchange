from decimal import Decimal, getcontext

from app.api.schemas.currency import Currency
from app.api.services.errors import BadCurrencyCode
from app.utils.external_api import get_currency

storage = dict()

class ExchangeService:
    @staticmethod
    def _save(data):
        for key, value in data.items():
            storage[key] = value

    @staticmethod
    async def _currency(code:str)->float|None:
        if len(storage)==0:       
            currency_json = await get_currency()   
            ExchangeService._save(currency_json["Valute"])

        currencies = storage
        currency = currencies.get(code.upper())
        if currency is None:
            return None
        c = float(currency["Value"])
        return c

    @staticmethod
    async def exchange(from_: str, to:str, value:float)->float:
        from_ = from_.upper()
        to = to.upper()
        getcontext().prec = 2
        from_value = await ExchangeService._currency(from_)
        if from_value is None:
            raise BadCurrencyCode(f"bad currency code: {from_}")
        to_value = await ExchangeService._currency(to)
        if to_value is None:
            raise BadCurrencyCode(f"bad currency code: {to}")
        return Decimal(from_value) / Decimal(to_value) * Decimal(value)
    
    @staticmethod
    async def available_currency()->list[Currency]:
        if len(storage)==0:
            currency_json = await get_currency()   
            ExchangeService._save(currency_json["Valute"])

        result = []
        for key, value in storage.items():
            result.append(Currency(code=key, name=value["Name"]))
        return result