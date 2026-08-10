from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password

from app.repositories.user_repository import (
    create_user,
    get_user_by_id,
    get_user_by_email,
    update_user,
    delete_user,
)

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)


def create_user_service(
    db: Session,
    user: UserCreate,
) -> UserResponse:

    # Check duplicate email
    existing_user = get_user_by_email(
        db,
        user.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Hash password
    hashed_password = hash_password(
        user.password
    )

    # Convert Pydantic model to dict
    user_data = user.model_dump()

    # Remove plain password
    user_data.pop("password")

    # Add hashed password
    user_data["hashed_password"] = hashed_password

    # Save user
    db_user = create_user(
        db,
        user_data,
    )

    return UserResponse.model_validate(db_user)


def get_user_service(
    db: Session,
    user_id: int,
) -> UserResponse | None:

    db_user = get_user_by_id(
        db,
        user_id,
    )

    if not db_user:
        return None

    return UserResponse.model_validate(db_user)


def update_user_service(
    db: Session,
    user_id: int,
    user_update: UserUpdate,
) -> UserResponse | None:

    updated_data = user_update.model_dump(
        exclude_unset=True
    )

    # If password is being updated,
    # hash it before saving.
    if "password" in updated_data:

        password = updated_data.pop("password")

        updated_data["hashed_password"] = hash_password(
            password
        )

    db_user = update_user(
        db,
        user_id,
        updated_data,
    )

    if not db_user:
        return None

    return UserResponse.model_validate(db_user)


def delete_user_service(
    db: Session,
    user_id: int,
) -> bool:

    return delete_user(
        db,
        user_id,
    )
    
    
def login_user_service(
    db: Session,
    email: str,
    password: str,
) -> UserResponse | None:

    db_user = get_user_by_email(
        db,
        email,
    )

    if not db_user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(
        password,
        db_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    access_token = create_access_token(
        data={"sub": str(db_user.id)}
    )
    
    refresh_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=60 * 60 * 24 * 7,  # 7 days
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }           