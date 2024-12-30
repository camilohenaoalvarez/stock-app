import logging
from typing import Self

from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.domain.schemas import BaseModel, Product, User
from app.infrastructure.configurations import Config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Stock:
    def __init__(self, db_engine):
        self._engine = db_engine

    @classmethod
    def from_config(cls, conf: Config) -> Self:
        engine = create_engine(conf.connection_string)
        return cls(engine)
    
    def init_db(self):
        try:
            BaseModel.metadata.create_all(self._engine)
            logger.info("Database initialized successfully")
        except Exception as err:
            logger.error(f"Error initializing database: {err}")


    # === Users ===

    def get_all_users(self) -> list[User]:
        try:
            with Session(self._engine) as session:
                stmt = select(User).options(joinedload(User.products))
                return session.execute(stmt).unique().scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching users with products: {e}")
            raise

    def get_user_by_id(self, user_id: int) -> User:
        try:
            with Session(self._engine) as session:
                stmt = select(User).options(joinedload(User.products)).filter_by(id=user_id)
                user = session.execute(stmt).scalars().first()
                if not user:
                    raise ValueError(f"User with id {user_id} does not exist")
                return user
        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by id {user_id}: {e}")
            raise

    def create_user(self, name: str) -> User:
        try:
            with Session(self._engine) as session:
                existing_user = session.execute(select(User).where(User.name == name)).scalar_one_or_none()
                if existing_user:
                    raise ValueError(f"User with name '{name}' already exists")
                
                new_user = User(name=name)
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                return new_user
        except IntegrityError as e:
            logger.error(f"Integrity error creating user: {e}")
            raise
        except SQLAlchemyError as e:
            logger.error(f"Error creating user: {e}")
            raise

    def delete_user_by_id(self, user_id: int) -> None:
        try:
            with Session(self._engine) as session:
                stmt = delete(User).where(User.id == user_id)
                result = session.execute(stmt)
                if result.rowcount == 0:
                    raise ValueError(f"User with id {user_id} does not exist")
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error deleting user by id {user_id}: {e}")
            raise

    def update_user(self, user_id: int, new_name: str) -> User:
        try:
            with Session(self._engine) as session:
                user = session.get(User, user_id)
                if not user:
                    raise ValueError(f"User with id {user_id} does not exist")
                
                # Check if the new name exists
                existing_user = session.execute(select(User).where(User.name == new_name, User.id != user_id)).scalar_one_or_none()
                if existing_user:
                    raise ValueError(f"Another user with name '{new_name}' already exists")

                user.name = new_name
                session.commit()
                session.refresh(user)
                return user
        except SQLAlchemyError as e:
            logger.error(f"Error updating user with id {user_id}: {e}")
            raise

    # === Products ===

    def get_all_products(self) -> list[Product]:
        try:
            with Session(self._engine) as session:
                stmt = select(Product).options(joinedload(Product.user))
                return session.execute(stmt).scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching products: {e}")
            raise

    def get_product_by_id(self, product_id: int) -> Product:
        try:
            with Session(self._engine) as session:
                product = session.get(Product, product_id)
                if not product:
                    raise ValueError(f"Product with id {product_id} does not exist")
                return product
        except SQLAlchemyError as e:
            logger.error(f"Error fetching product by id {product_id}: {e}")
            raise

    def create_product(self, name: str, user_id: int) -> Product:
        try:
            with Session(self._engine) as session:
                existing_product = session.execute(select(Product).where(Product.name == name)).scalar_one_or_none()
                if existing_product:
                    raise ValueError(f"Product with name '{name}' already exists")
                
                new_product = Product(name=name)
                if user_id:
                    user = session.get(User, user_id)
                    if not user:
                        raise ValueError(f"User with id {user_id} does not exist")
                    new_product.user_id = user_id

                session.add(new_product)
                session.commit()
                session.refresh(new_product)
                return new_product
        except IntegrityError as e:
            logger.error(f"Integrity error creating product: {e}")
            raise
        except SQLAlchemyError as e:
            logger.error(f"Error creating product: {e}")
            raise

    def delete_product_by_id(self, product_id: int) -> None:
        try:
            with Session(self._engine) as session:
                stmt = delete(Product).where(Product.id == product_id)
                result = session.execute(stmt)
                if result.rowcount == 0:
                    raise ValueError(f"Product with id {product_id} does not exist")
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error deleting product by id {product_id}: {e}")
            raise

    def update_product(self, product_id: int, new_name: str, new_user_id: int) -> Product:
        try:
            with Session(self._engine) as session:
                product = session.get(Product, product_id)
                if not product:
                    raise ValueError(f"Product with id {product_id} does not exist")
                
                # Check if the new name exists
                existing_product = session.execute(select(Product).where(Product.name == new_name, Product.id != product_id)).scalar_one_or_none()
                if existing_product:
                    raise ValueError(f"Another product with name '{new_name}' already exists")
                
                # Validate the new user ID
                if new_user_id:
                    user = session.get(User, new_user_id)
                    if not user:
                        raise ValueError(f"User with id {new_user_id} does not exist")
                    product.user_id = new_user_id

                product.name = new_name

                session.commit()
                session.refresh(product)
                return product
        except SQLAlchemyError as e:
            logger.error(f"Error updating product with id {product_id}: {e}")
            raise
