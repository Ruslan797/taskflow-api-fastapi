from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.users import User
from app.schemas.users import UserCreate


class UserAlreadyExistsError(Exception):
    """Raised when a user with the same email already exists."""


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = select(User).where(
        User.email == email,
    )

    return db.scalar(statement)


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    existing_user = get_user_by_email(
        db,
        str(user_data.email),
    )

    if existing_user is not None:
        raise UserAlreadyExistsError

    user = User(
        email=str(user_data.email),
        hashed_password=hash_password(
            user_data.password,
        ),
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise UserAlreadyExistsError from error

    db.refresh(user)

    return user