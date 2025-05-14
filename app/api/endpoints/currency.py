from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.api.models.user import User
from app.api.schemas.currency import Currency
from app.api.services.errors import BadCurrencyCode
from app.api.services.exchange import ExchangeService
from app.core.security import get_current_user


router = APIRouter(prefix='/currency')

@router.get("/list")
async def list(_:Annotated[User, Depends(get_current_user)])->list[Currency]:
    return await ExchangeService.available_currency()

@router.get("/exchange/{from_:str}/{to:str}")
async def exchange(_:Annotated[User, Depends(get_current_user)],
                    from_:str, to:str, value:float=1)->float:
    try:
        return await ExchangeService.exchange(from_, to, value)
    except BadCurrencyCode as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(err))