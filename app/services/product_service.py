from sqlalchemy.orm import Session
from app.models.product import Product
from app.repositories.product_repository import (
    get_products,
    get_product,
    create_product,
    update_product,
    delete_product,
)
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)


def get_products_service(db: Session) -> list[ProductResponse]:
    db_products = get_products(db)
    return [ProductResponse.model_validate(product) for product in db_products]

def get_product_service(db: Session, product_id: int) -> ProductResponse | None:
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    return ProductResponse.model_validate(db_product)

def create_product_service(db: Session, product: ProductCreate) -> ProductResponse:
    db_product = create_product(db, product)
    return ProductResponse.model_validate(db_product)

def update_product_service(db: Session, product_id: int, product_update: ProductUpdate) -> ProductResponse | None:
    db_product = update_product(db, product_id, product_update)
    if not db_product:
        return None
    return ProductResponse.model_validate(db_product)

def delete_product_service(db: Session, product_id: int) -> bool:
    return delete_product(db, product_id)