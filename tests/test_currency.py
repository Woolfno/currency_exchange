from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient

mock_currency_json = {
    "Valute": {
        "USD": {
            "ID": "R01235",
            "NumCode": "840",
            "CharCode": "USD",
            "Nominal": 1,
            "Name": "Доллар США",
            "Value": 84.64,
            "Previous": 84.3955
        },
        "EUR": {
            "ID": "R01239",
            "NumCode": "978",
            "CharCode": "EUR",
            "Nominal": 1,
            "Name": "Евро",
            "Value": 91.4262,
            "Previous": 92.4633
        },
    }
}


def mock_external_api(mock_get):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = mock_currency_json
    mock_get.return_value.__aenter__.return_value = mock_response


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_get_currency_list(mock_get: MagicMock, access_token: str, client: AsyncClient):
    mock_external_api(mock_get)
    response = await client.get('/currency/list',
                                headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json() == [{"code": "USD", "name": "Доллар США"},
                               {"code": "EUR", "name": "Евро"},
                               ]


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_exchange_currency(mock_get: MagicMock, access_token: str, client: AsyncClient):
    mock_external_api(mock_get)
    from_ = "usd"
    to = "eur"
    value = "1"
    url = f"/currency/exchange/{from_}/{to}?value={value}"
    response = await client.get(url,
                                headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.text == "0.93"


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_exchange_bad_currency(mock_get: MagicMock, access_token: str, client: AsyncClient):
    mock_external_api(mock_get)
    from_ = "QWE"
    to = "eur"
    value = "1"
    url = f"/currency/exchange/{from_}/{to}?value={value}"
    response = await client.get(url,
                                headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 400
    assert response.json()['detail'] == "bad currency code: QWE"
