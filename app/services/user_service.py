from sqlalchemy.orm import Session

from app.repositories.user_repository import (
    create_user,
    get_user_by_id,
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
    db_user = create_user(db, user)

    return UserResponse.model_validate(db_user)


def get_user_service(
    db: Session,
    user_id: int,
) -> UserResponse | None:
    db_user = get_user_by_id(db, user_id)

    if not db_user:
        return None

    return UserResponse.model_validate(db_user)


def update_user_service(
    db: Session,
    user_id: int,
    user_update: UserUpdate,
) -> UserResponse | None:
    db_user = update_user(
        db,
        user_id,
        user_update,
    )

    if not db_user:
        return None

    return UserResponse.model_validate(db_user)


def delete_user_service(
    db: Session,
    user_id: int,
) -> bool:
    return delete_user(db, user_id)