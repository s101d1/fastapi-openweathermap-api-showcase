import uuid

from sqlalchemy import DateTime, func, Uuid
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    id = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, sort_order=-1)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), sort_order=-1)
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now(), sort_order=-1)
