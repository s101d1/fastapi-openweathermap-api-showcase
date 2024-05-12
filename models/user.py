from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    user_name = mapped_column(String(255), unique=True, nullable=False)
    password = mapped_column(String(60), nullable=False)
    preference: Mapped["UserPreference"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return (f"User("
                f"id={self.id!r}"
                f", created_at={self.created_at!r}"
                f", updated_at={self.updated_at!r}"
                f", user_name={self.user_name!r}"
                f")")
