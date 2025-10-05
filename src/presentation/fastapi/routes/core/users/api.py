from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.users import CreateUserSchema, UserSchemas
from src.usecase.users.create import CreateUserUsecase
from src.usecase.users.get_all import GetUsersUsecase

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_users(usecase: FromDishka[GetUsersUsecase]) -> list[UserSchemas]:
    return await usecase()

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_users(
    usecase: FromDishka[CreateUserUsecase],
    user: CreateUserSchema) -> None:
    await usecase(user)
