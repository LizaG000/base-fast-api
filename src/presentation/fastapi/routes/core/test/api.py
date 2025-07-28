from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_test() -> str:
    return "УРАААААА"
