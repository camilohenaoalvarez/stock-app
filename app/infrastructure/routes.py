"""Endpoints file that look for data in the Stock DB"""

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.domain.schemas import Product, User
from app.domain.models import ProductCreate, ProductSchema, ProductUpdate, UserCreate, UserSchema, UserUpdate

from app.infrastructure.repositories import Stock

router = APIRouter()

def get_db_client(request: Request) -> Stock:
    """Get the db client from the current app state"""
    return request.app.state.db_client


# User Endpoints

@router.get("/users/", response_model=list[UserSchema])
async def get_users(db_client: Stock = Depends(get_db_client)):
    try:
        return db_client.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db_client: Stock = Depends(get_db_client)):
    try:
        return db_client.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db_client: Stock = Depends(get_db_client)):
    try:
        return db_client.create_user(user_data.name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate, db_client: Stock = Depends(get_db_client)):
    try:
        return db_client.update_user(user_id, user_data.new_name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db_client: Stock = Depends(get_db_client)):
    try:
        db_client.delete_user_by_id(user_id)
        return
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Product Endpoints

@router.get("/products/", response_model=list[ProductSchema])
async def get_products(db_client: Stock = Depends(get_db_client)):
    try:
        return db_client.get_all_products()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/products/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db_client: Stock = Depends(get_db_client)):
    try:
        return db_client.get_product_by_id(product_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/products/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, db_client: Stock = Depends(get_db_client)):
    try:
        return db_client.create_product(product_data.name, product_data.user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/products/{product_id}", response_model=ProductSchema)
async def update_product(product_id: int, product_data: ProductUpdate, db_client: Stock = Depends(get_db_client)):
    try:
        return db_client.update_product(product_id, product_data.new_name, product_data.new_user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db_client: Stock = Depends(get_db_client)):
    try:
        db_client.delete_product_by_id(product_id)
        return
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
