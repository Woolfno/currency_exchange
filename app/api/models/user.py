from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import types, text
from app.database.db import Base


class User(Base):
    __tablename__ = "user"

    id:Mapped[UUID] = mapped_column(type_=types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    username:Mapped[str] = mapped_column(unique=True)
    password:Mapped[str]
