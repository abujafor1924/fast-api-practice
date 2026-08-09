from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import user as user_routes
from app.api.routes import product as product_routes

from app.db.base import Base
from app.db.session import engine

# Register models
from app.models.user import User


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="1.0.0",
)


app.include_router(
    user_routes.router,
    prefix=settings.API_V1_STR,
)


app.include_router(
    product_routes.router,
    prefix=settings.API_V1_STR,
)

@app.get("/")
def home():
    return {
        "message": "Welcome to FastAPI!",
        "app_name": settings.APP_NAME,
        "api_version": settings.API_V1_STR,
    }
    
@app.get("/products")
def get_products():
    return {"message": "This endpoint will return a list of products."}