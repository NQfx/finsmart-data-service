from fastapi import APIRouter, Depends, HTTPException, Query

from api.dependecies import get_session, get_user_id
from repositories import user_data as user_data_rep
import schemes.user_data as user_data_schemes
import models.user_data as user_data_models
import uuid

router = APIRouter(tags=["Users"])

@router.post("/")
async def create_user(user_uuid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.UserRepository(session)
    user = await repo.insert_user(user_uuid)
    return user_data_schemes.UserOut.model_validate(user)

@router.get("/{user_uuid}")
async def get_user(
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.UserRepository(session)
    user = await repo.select_user(user_id)
    return user_data_schemes.UserOut.model_validate(user)

@router.get("/")
async def get_users(
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.UserRepository(session)
    users = await repo.select_users()
    return [user_data_schemes.UserOut.model_validate(user) for user in users]


@router.delete("/{user_uuid}")
async def delete_user(
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.UserRepository(session)
    if not  await repo.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")

accounts_router = APIRouter(tags=["Accounts"])
router.include_router(accounts_router)

@accounts_router.get("/{user_uuid}/accounts")
async def get_accounts(
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.AccountRepository(session)
    accounts = await repo.select_accounts(user_id)
    return [user_data_schemes.AccountOut.model_validate(acc) for acc in accounts]

@accounts_router.get("/accounts/{account_id}")
async def get_account(
    account_id: int,
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.AccountRepository(session)
    accounts = await repo.select_account(account_id)
    return user_data_schemes.AccountOut.model_validate(accounts)

@accounts_router.post("/{user_uuid}/accounts")
async def create_account(
    data: user_data_schemes.AccountCreate,
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.AccountRepository(session)
    account = await repo.insert_account(**data.model_dump(), user_id=user_id)
    return user_data_schemes.AccountOut.model_validate(account)

@accounts_router.patch("/{user_uuid}/accounts/{account_id}")
async def update_account(
    account_id: int,
    data: user_data_schemes.AccountUpdate,
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.AccountRepository(session)
    account = await repo.update_account(**data.model_dump(), user_id=user_id, account_id=account_id)
    return user_data_schemes.AccountOut.model_validate(account)

@accounts_router.delete("/accounts/{account_id}")
async def delete_account(
    account_id: int,
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.AccountRepository(session)
    if not await repo.delete_account(account_id):
        raise HTTPException(status_code=404, detail="Account not found")

@accounts_router.get("/accounts/{account_id}/transactions")
async def get_account_transactions(
    account_id: int,
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.TransactionRepository(session)
    txs = await repo.select_transactions(account_id=account_id)
    return [user_data_schemes.TransactionOut.model_validate(tx) for tx in txs]

transactions_router = APIRouter(tags=["Transactons"])
router.include_router(transactions_router)

@transactions_router.post("/{user_uuid}/transactions")
async def create_transaction(
    data: user_data_schemes.TransactionCreate,
    goal_id: int | None = Query(default=None),
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.TransactionRepository(session)
    tx = await repo.insert_transaction(
        **data.model_dump(),
        user_id=user_id,
        goal_id=goal_id,
    )
    return user_data_schemes.TransactionOut.model_validate(tx)

@transactions_router.get("/{user_uuid}/transactions")
async def get_transactions(
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.TransactionRepository(session)
    txs = await repo.select_transactions(user_id=user_id)
    return [user_data_schemes.TransactionOut.model_validate(tx) for tx in txs]

@transactions_router.get("/transactions/{transaction_id}")
async def get_transaction(
    transaction_id: int,
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.TransactionRepository(session)
    tx = await repo.select_transaction(transaction_id)
    if tx is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return user_data_schemes.TransactionOut.model_validate(tx)

@transactions_router.patch("/{user_uuid}/transactions/{transaction_id}")
async def update_transaction(
    transaction_id: int,
    data: user_data_schemes.TransactionUpdate,
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.TransactionRepository(session)
    tx = await repo.update_transaction(
        **data.model_dump(),
        user_id=user_id,
        transaction_id=transaction_id,
    )
    if tx is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return user_data_schemes.TransactionOut.model_validate(tx)

@transactions_router.delete("/transactions/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.TransactionRepository(session)
    if not await repo.delete_transaction(transaction_id):
        raise HTTPException(status_code=404, detail="Transaction not found")

goals_router = APIRouter(tags=["Goals"])
router.include_router(goals_router)

@goals_router.post("/{user_uuid}/goals")
async def create_goal(
    data: user_data_schemes.GoalCreate,
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.GoalRepository(session)
    goal = await repo.insert_goal(**data.model_dump(), user_id=user_id)
    return user_data_schemes.GoalOut.model_validate(goal)

@goals_router.get("/{user_uuid}/goals")
async def get_goals(
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.GoalRepository(session)
    goals = await repo.select_goals(user_id=user_id)
    return [user_data_schemes.GoalOut.model_validate(goal) for goal in goals]

@goals_router.get("/goals/{goal_id}")
async def get_goal(
    goal_id: int,
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.GoalRepository(session)
    goal = await repo.select_goal(goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return user_data_schemes.GoalOut.model_validate(goal)

@goals_router.patch("/{user_uuid}/goals/{goal_id}")
async def update_goal(
    goal_id: int,
    data: user_data_schemes.GoalUpdate,
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.GoalRepository(session)
    goal = await repo.update_goal(**data.model_dump(), user_id=user_id, goal_id=goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return user_data_schemes.GoalOut.model_validate(goal)

@goals_router.delete("/goals/{goal_id}")
async def delete_goal(
    goal_id: int,
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.GoalRepository(session)
    if not await repo.delete_goal(goal_id):
        raise HTTPException(status_code=404, detail="Goal not found")

@goals_router.get("/goals/{goal_id}/transactions")
async def get_goal_transactions(
    goal_id: int,
    session: AsyncSession = Depends(get_session),
):
    repo = user_data_rep.TransactionRepository(session)
    txs = await repo.select_transactions(goal_id=goal_id)
    return [user_data_schemes.TransactionOut.model_validate(tx) for tx in txs]

