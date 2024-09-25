from database import new_session, UserOrm, ProductOrm
from schemas import *
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

class UserRepository:
    @classmethod
    async def select_all(cls) -> SUser:
        async with new_session() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            users_models = result.scalars().all()
            return users_models
    @classmethod
    async def add_user(cls, data : SUser) -> SUser:
        async with new_session() as session:
            user_dict = data.model_dump()
            user = UserOrm(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return {"message" : "Пользователь был создан", "data" : user}
    @classmethod
    async def check_user(cls, user_login : str, user_password : str) -> SUser:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.login == user_login and UserOrm.password == user_password)
            result = await session.execute(query)
            user_model = result.scalars().all()
            return user_model
    @classmethod
    async def update_user(cls, id : int, data : SUserAdd) -> SUser:
        async with new_session() as session:
            query = update(UserOrm).values(
                email = data.email,
                login = data.login,
                password = data.password,
                phone_number = data.phone_number,
                mail_index = data.mail_index,
                region = data.region,
                rating = data.rating,
                role = data.role).where(UserOrm.id == id)
            await session.execute(query)
            await session.commit()
            
            query2 = select(UserOrm).where(UserOrm.id == id)
            result = await session.execute(query2)
            changed_user = result.scalars().all()
            return changed_user
                       
class ProductRepository:
    @classmethod
    async def select_all(cls) -> SProduct:
        async with new_session() as session:
            query = select(ProductOrm).options(joinedload(ProductOrm.creator)).options(joinedload(ProductOrm.buyer))
            result = await session.execute(query)
            products_models = result.scalars().all()
            return products_models
    @classmethod
    async def add_product(cls, data : SProductAdd) -> SProduct:
        async with new_session() as session:
            product_dict = data.model_dump()
            product = ProductOrm(**product_dict)
            session.add(product)
            await session.flush()
            await session.commit()
            return {"message" : "Товар был создан", "data" : product}
    @classmethod
    async def update_product(cls, prod_id : int, data : SProductAdd):
        async with new_session() as session:
            product = await session.get(ProductOrm, prod_id)
            product.product_name = data.product_name
            product.product_description = data.product_description
            product.price = data.price
            product.creator_id = data.creator_id
            product.buyer_id = data.buyer_id
            product.status = data.status
            await session.refresh(product)
            await session.commit()
            
            query2 = select(ProductOrm).where(ProductOrm.product_id == prod_id)
            result = await session.execute(query2)
            changed_user = result.scalars().all()
            return changed_user
    @classmethod
    async def delete_product(cls, prod_id : int):
        async with new_session() as session:
            product = await session.get(ProductOrm, prod_id)
            if product.status == ProductStatus.recieved or product.status == ProductStatus.shipped:
                return f"Товар невозможно удалить, так как он уже либо отправлен, либо получен"
            await session.delete(product)
            await session.commit()

            return "Товар был удалён"
            