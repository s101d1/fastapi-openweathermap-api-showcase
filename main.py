from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse

from database import engine
from models.base import Base
from models.user import User
from models.user_preference import UserPreference
from routes.users import router as users_router


def init_db():
    """
        Initialize database by creating the tables if they don't exist yet (for development purpose only)
    """
    Base.metadata.create_all(engine)
    print("Initialized the database")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
        FastAPI lifespan manager
    """
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(_request, exc):
    """
        Reformat RequestValidationError json response with message field on top
    """
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content={"message": exc.errors()[0]["msg"], "errors": jsonable_encoder(exc.errors())})


@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(_request, exc):
    """
        Reformat ResponseValidationError json response with message field on top
    """
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content={"message": exc.errors()[0]["msg"], "errors": jsonable_encoder(exc.errors())})


app.include_router(users_router)
