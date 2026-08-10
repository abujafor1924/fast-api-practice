from sqlalchemy.orm import Session

from app.models.user import User


def create_user(db: Session, user_data: dict):
    db_user = User(
        username=user_data["username"],
        email=user_data["email"],
        hashed_password=user_data["hashed_password"],
        role="user",
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_email(db: Session, email: str) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def update_user(
    db: Session,
    user_id: int,
    user_update: dict,
) -> User | None:

    db_user = get_user_by_id(db, user_id)

    if not db_user:
        return None

    update_data = user_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(
    db: Session,
    user_id: int,
) -> bool:

    db_user = get_user_by_id(db, user_id)

    if not db_user:
        return False

    db.delete(db_user)
    db.commit()

    return True