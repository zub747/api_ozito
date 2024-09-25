import enum
from typing import Optional, List
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey, Float, Date, Boolean
from datetime import date

engine = create_async_engine(
    "sqlite+aiosqlite:///tasks.db"
)

new_session = async_sessionmaker(engine, expire_on_commit = False)

class Model(DeclarativeBase):
    pass

class Role(enum.Enum):
    user = "user"
    admin = "admin"

class UserOrm(Model):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    email : Mapped[str] = mapped_column(String, nullable=False)
    login : Mapped[str] = mapped_column(String, nullable=False)
    password : Mapped[str] = mapped_column(String, nullable=False)
    phone_number : Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mail_index : Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    region : Mapped[str] = mapped_column(String, nullable=False)
    rating : Mapped[Optional[int]] = mapped_column(Float, nullable=True, default=0)
    role : Mapped[Role] = mapped_column(default=Role.user)
    is_active : Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class ProductStatus(enum.Enum):
    listed = "Выставлен"
    shipped = "Отправлен"
    recieved = "Получен"
    
class ProductOrm(Model):
    __tablename__ = "products"
    product_id : Mapped[int] = mapped_column(Integer, primary_key = True)
    product_name : Mapped[str] = mapped_column(String, nullable=False)
    product_description : Mapped[str] = mapped_column(String, nullable=False)
    price : Mapped[int] = mapped_column(Integer, nullable=False)
    creator_id : Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    creator : Mapped["UserOrm"] = relationship("UserOrm", foreign_keys=[creator_id])
    buyer_id : Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    buyer : Mapped["UserOrm"] = relationship("UserOrm", foreign_keys=[buyer_id])
    created_at : Mapped[date] = mapped_column(Date, default=date.today)
    status : Mapped[ProductStatus] = mapped_column(default=ProductStatus.listed)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)