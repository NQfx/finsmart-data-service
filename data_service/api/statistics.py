from fastapi import APIRouter

router = APIRouter(tags=["Statistics"])

@router.get('/{user_uuid}/dashboard')
async def get_dashboard(user_uuid: str):
    return {"message": f"Hi, {user_uuid}!"}


@router.get('/{user_uuid}/balance')
async def get_balance(user_uuid: str):
    ...


@router.get('/{user_uuid}/income-expense')
async def get_income_expense(user_uuid: str):
    ...


@router.get('/{user_uuid}/top-categories')
async def get_top_categories(user_uuid: str):
    ...


@router.get('/{user_uuid}/timeseries')
async def get_timeseries(user_uuid: str):
    ...
