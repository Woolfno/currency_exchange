from decimal import Decimal, getcontext

from app.api.schemas.currency import Currency
from app.api.services.errors import BadCurrencyCode
from app.utils.external_api import get_currency


class ExchangeService:
    def __init__(self) -> None:
        self._storage = dict()

    async def load_currency(self) -> None:
        currencies = dict()
        currency_json = await get_currency()        
        for key, value in currency_json["Valute"].items():
            currencies[key] = value
        self._storage = currencies

    def exchange(self, from_: str, to: str, value: float) -> float:
        from_ = from_.upper()
        to = to.upper()
        getcontext().prec = 2
        from_value = self._storage.get(from_)
        if from_value is None:
            raise BadCurrencyCode(f"bad currency code: {from_}")
        to_value = self._storage.get(to)
        if to_value is None:
            raise BadCurrencyCode(f"bad currency code: {to}")
        return Decimal(from_value) / Decimal(to_value) * Decimal(value)

    def available_currency(self) -> list[Currency]:
        result = []
        for key, value in self._storage.items():
            result.append(Currency(code=key, name=value["Name"]))
        return result

async def get_exchange_service()->ExchangeService:
    service = ExchangeService()
    await service.load_currency()
    return service