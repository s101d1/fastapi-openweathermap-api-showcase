from uuid import UUID

from fastapi import APIRouter, Response, status, Path

from controllers.user import create_user, get_user, update_user_preference, get_user_weather, get_user_forecast_best_day
from models.dto.user import CreateUserData, UserData, UserPreferenceData

router = APIRouter(prefix="/users")


@router.post("/", tags=["users"])
async def create_user_route(data: CreateUserData, response: Response):
    """
        Create a new user
    """
    response.status_code = status.HTTP_201_CREATED
    return create_user(data)


@router.get("/{user_id}", tags=["users"])
async def get_user_route(user_id: UUID = Path(title="The User ID")) -> UserData:
    """
        Find user by id and return its detail and preference data
    """
    return get_user(user_id)


@router.put("/{user_id}/preference", tags=["users"])
async def put_user_preference_route(data: UserPreferenceData, user_id: UUID = Path(title="The User ID")):
    """
        Update user preference
    """
    return update_user_preference(user_id, data)


@router.get("/{user_id}/weather", tags=["users"])
async def get_user_weather_route(user_id: UUID = Path(title="The User ID")):
    """
        Get current weather data for a user
    """
    return get_user_weather(user_id)


@router.get("/{user_id}/forecast-best-day", tags=["users"])
async def get_user_forecast_best_day_route(user_id: UUID = Path(title="The User ID")):
    """
        Find the recommended best day from 5-day weather forecast for a user
    """
    return get_user_forecast_best_day(user_id)
