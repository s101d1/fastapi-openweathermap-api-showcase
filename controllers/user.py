import json
from uuid import UUID

from fastapi import HTTPException, status
from pyowm.commons.exceptions import APIRequestError, PyOWMError
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from database import session
from models.dto.user import CreateUserData, UserPreferenceData
from models.user import User
from models.user_preference import UserPreference
from services.forecast import forecast_best_day
from utils.auth import get_hashed_password
from utils.owm_client import get_weather_at_place


def create_user(data: CreateUserData):
    """
        Create a new user
    """

    existing_user = session.execute(select(User).where(User.user_name == data.user_name)).scalar_one_or_none()
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User name already exists")

    if data.password != data.confirm_password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Confirm Password doesn't match")

    # Hash the password with bcrypt
    hashed_password = get_hashed_password(data.password)

    # Create the user
    new_user = User(user_name=data.user_name, password=hashed_password, preference=UserPreference())
    session.add(new_user)
    session.commit()

    return {"message": "User created", "id": new_user.id}


def get_user(user_id: UUID):
    """
        Find a User by id and return the user and its preferences data
    """

    user = session.execute(
        select(User).options(selectinload(User.preference)).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")

    return user


def update_user_preference(user_id: UUID, data: UserPreferenceData):
    """
        Update user preference
    """

    user = session.execute(
        select(User).options(selectinload(User.preference)).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")

    data.location = data.location.strip() if data.location is not None else data.location

    if data.location is not None and data.location == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid location value")

    if data.temp_min is not None and data.temp_max is not None and data.temp_min > data.temp_max:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid temperature min value")

    if data.max_cloudiness is not None and data.max_cloudiness < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid max cloudiness value")

    if data.max_wind_speed is not None and data.max_wind_speed < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid max wind speed value")

    if data.max_rain_volume is not None and data.max_rain_volume < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid max rain volume value")

    if data.max_snow_volume is not None and data.max_snow_volume < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid max snow volume value")

    preference_data = {
        "location": data.location,
        "temp_min": data.temp_min,
        "temp_max": data.temp_max,
        "max_cloudiness": data.max_cloudiness,
        "max_wind_speed": data.max_wind_speed,
        "max_rain_volume": data.max_rain_volume,
        "max_snow_volume": data.max_snow_volume
    }
    user_preference = session.execute(
        select(UserPreference).where(UserPreference.user_id == user_id)).scalar_one_or_none()
    if user_preference is not None:
        session.execute(update(UserPreference).where(UserPreference.user_id == user_id).values(**preference_data))
    else:
        session.add(UserPreference(user_id=user_id, **preference_data))

    session.commit()

    return {"message": "User preference updated"}


def get_user_weather(user_id: UUID):
    """
        Get weather data for a user
    """

    user = session.execute(
        select(User).options(selectinload(User.preference)).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")

    user_preference = session.execute(
        select(UserPreference).where(UserPreference.user_id == user_id)).scalar_one_or_none()
    if user_preference is None:
        print("An error occured: missing preference")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured")

    if user_preference.location is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Location is not set")

    try:
        return get_weather_at_place(user_preference.location)
    except APIRequestError as err:
        req_error = json.loads(str(err))
        raise HTTPException(status_code=int(req_error["cod"]), detail=req_error["message"])
    except PyOWMError as err:
        print("An error occured: ", err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured")


def get_user_forecast_best_day(user_id: UUID):
    """
        Find the recommended best day from 5-day weather forecast based on a user's weather preference
    """

    user = session.execute(
        select(User).options(selectinload(User.preference)).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")

    user_preference = session.execute(
        select(UserPreference).where(UserPreference.user_id == user_id)).scalar_one_or_none()
    if user_preference is None:
        print("An error occured: missing preference")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured")

    if user_preference.location is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Location is not set")

    try:
        best_day = forecast_best_day(user_preference)
        if best_day is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No best day")

        return {"best_day": best_day}
    except APIRequestError as err:
        req_error = json.loads(str(err))
        raise HTTPException(status_code=int(req_error["cod"]), detail=req_error["message"])
    except PyOWMError as err:
        print("An error occured: ", err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured")
