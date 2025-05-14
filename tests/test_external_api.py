import pytest
from app.utils.external_api import get_currency
from app.utils.errors import CurrencyNotAvailableError

@pytest.mark.asyncio
async def test_external_api():
    currency = await get_currency()
    assert len(currency)>0

@pytest.mark.asyncio
async def test_external_api_bad():
    with pytest.raises(CurrencyNotAvailableError):
        currency = await get_currency()
