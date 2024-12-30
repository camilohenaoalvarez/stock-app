from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship

class BaseModel(DeclarativeBase, MappedAsDataclass):
    pass

class User(BaseModel):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    products = relationship("Product", back_populates="user", passive_deletes=True)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"

class Product(BaseModel):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, init=False)
    
    user = relationship("User", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, user_id={self.user_id})>"
