from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import (
    get_products_service,
    get_product_service,
    create_product_service,
    update_product_service,
    delete_product_service,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)   

@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return get_products_service(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_service(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product_service(db, product)  

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product_service(db, product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = delete_product_service(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None