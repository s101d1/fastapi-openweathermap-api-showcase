from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class CreateUserData(BaseModel):
    user_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=15, to_lower=True)]
    password: str
    confirm_password: str


class UserPreferenceData(BaseModel):
    location: str | None
    temp_min: float | None
    temp_max: float | None
    max_cloudiness: float | None
    max_wind_speed: float | None
    max_rain_volume: float | None
    max_snow_volume: float | None


class UserData(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime | None
    user_name: str
    preference: UserPreferenceData
