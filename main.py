from fastapi import FastAPI
from app.api.endpoints import currencyRouter, userRouter


app = FastAPI()
app.include_router(userRouter)
app.include_router(currencyRouter)