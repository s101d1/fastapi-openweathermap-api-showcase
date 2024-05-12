from sqlalchemy import String, Double, ForeignKey, Uuid, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    location = mapped_column(Text)
    # measurement_units = mapped_column(String(50))
    temp_min = mapped_column(Double)
    temp_max = mapped_column(Double)
    max_cloudiness = mapped_column(Double)
    max_wind_speed = mapped_column(Double)
    max_rain_volume = mapped_column(Double)
    max_snow_volume = mapped_column(Double)
    user_id: Mapped[Uuid] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="preference")

    def __repr__(self) -> str:
        return (f"UserPreference("
                f"id={self.id!r}"
                f", created_at={self.created_at!r}"
                f", updated_at={self.updated_at!r}"
                f", location={self.location!r}"
                # f", measurement_units={self.measurement_units!r}"
                f", temp_min={self.temp_min!r}"
                f", temp_max={self.temp_max!r}"
                f", max_cloudiness={self.max_cloudiness!r}"
                f", max_wind_speed={self.max_wind_speed!r}"
                f", max_rain_volume={self.max_rain_volume!r}"
                f", max_snow_volume={self.max_snow_volume!r}"
                f")")
