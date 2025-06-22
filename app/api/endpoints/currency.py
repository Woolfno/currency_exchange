from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.api.models.user import User
from app.api.schemas.currency import Currency
from app.api.services.errors import BadCurrencyCode
from app.api.services.exchange import ExchangeService, get_exchange_service
from app.core.security import get_current_user

router = APIRouter(prefix='/currency')


@router.get("/list")
async def list(_: Annotated[User, Depends(get_current_user)],
               service: Annotated[ExchangeService, Depends(get_exchange_service)],
               ) -> list[Currency]:
    return service.available_currency()


@router.get("/exchange/{from_:str}/{to:str}")
async def exchange(_: Annotated[User, Depends(get_current_user)],
                   service: Annotated[ExchangeService, Depends(get_exchange_service)],
                   from_: str, to: str, value: float = 1) -> float:
    try:
        return service.exchange(from_, to, value)
    except BadCurrencyCode as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(err))
