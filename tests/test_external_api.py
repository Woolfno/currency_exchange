import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.utils.external_api import get_currency
from app.utils.errors import CurrencyNotAvailableError


@pytest.mark.asyncio
async def test_external_api():
    currency = await get_currency()
    assert len(currency)>0

@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_external_api_bad(mock_get:MagicMock):
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_get.return_value.__aenter__.return_value = mock_response
    with pytest.raises(CurrencyNotAvailableError):
        currency = await get_currency()
