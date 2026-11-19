import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_session
from models.user_data import (
    User,
    Account,
    Transaction,
    Contract,
    Goal,
    AccountType,
    TransactionCategory,
    ContractKind,
)


def _apply_updates(obj, fields: dict) -> None:
    for key, value in fields.items():
        if hasattr(obj, key) and value:
            setattr(obj, key, value)


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


class UserRepository(BaseRepository):
    async def get_id_by_uuid(self, user_uuid: uuid.UUID) -> int | None:
        return await self.session.scalar(
            select(User.id).where(User.uuid == user_uuid)
        )

    async def insert_user(self, user_uuid: uuid.UUID) -> User:
        user = User(uuid=user_uuid)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def select_user(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def select_users(self) -> list[User]:
        result = await self.session.scalars(select(User))
        return list(result)

    async def delete_user(self, user_id: int) -> bool:
        user = await self.session.get(User, user_id)
        if user is None:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True


class AccountRepository(BaseRepository):
    async def insert_account(
        self,
        user_id: int,
        name: str,
        type: AccountType,
        balance: Decimal,
    ) -> Account:
        account = Account(user_id=user_id, name=name, type=type, balance=balance)
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def select_account(self, account_id: int) -> Account | None:
        return await self.session.get(Account, account_id)

    async def select_accounts(self, user_id: Optional[int] = None) -> list[Account]:
        stmt = select(Account)
        if user_id is not None:
            stmt = stmt.where(Account.user_id == user_id)
        return list(await self.session.scalars(stmt))

    async def update_account(self, account_id: int, **fields) -> Account | None:
        account = await self.session.get(Account, account_id)
        if account is None:
            return None
        _apply_updates(account, fields)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def delete_account(self, account_id: int) -> bool:
        account = await self.session.get(Account, account_id)
        if account is None:
            return False
        await self.session.delete(account)
        await self.session.commit()
        return True


class TransactionRepository(BaseRepository):
    async def insert_transaction(
        self,
        user_id: int,
        amount: Decimal,
        ts: datetime,
        balance: Decimal,
        category: TransactionCategory,
        account_id: Optional[int] = None,
        goal_id: Optional[int] = None,
    ) -> Transaction:
        tx = Transaction(
            user_id=user_id,
            account_id=account_id,
            amount=amount,
            ts=ts,
            balance=balance,
            category=category,
            goal_id=goal_id,
        )
        self.session.add(tx)
        await self.session.commit()
        await self.session.refresh(tx)
        return tx

    async def select_transaction(self, transaction_id: int) -> Transaction | None:
        return await self.session.get(Transaction, transaction_id)

    async def select_transactions(
        self,
        user_id: Optional[int] = None,
        account_id: Optional[int] = None,
        goal_id: Optional[int] = None,
    ) -> list[Transaction]:
        stmt = select(Transaction)
        if user_id is not None:
            stmt = stmt.where(Transaction.user_id == user_id)
        if account_id is not None:
            stmt = stmt.where(Transaction.account_id == account_id)
        if goal_id is not None:
            stmt = stmt.where(Transaction.goal_id == goal_id)
        return list(await self.session.scalars(stmt))

    async def update_transaction(self, transaction_id: int, **fields) -> Transaction | None:
        tx = await self.session.get(Transaction, transaction_id)
        if tx is None:
            return None
        _apply_updates(tx, fields)
        await self.session.commit()
        await self.session.refresh(tx)
        return tx

    async def delete_transaction(self, transaction_id: int) -> bool:
        tx = await self.session.get(Transaction, transaction_id)
        if tx is None:
            return False
        await self.session.delete(tx)
        await self.session.commit()
        return True


class ContractRepository(BaseRepository):
    async def insert_contract(
        self,
        account_id: int,
        kind: ContractKind,
        rate: Decimal,
        principal_amount: Optional[Decimal] = None,
        maturity_date: Optional[date] = None,
        compounding: Optional[str] = None,
        payment_amount: Optional[Decimal] = None,
    ) -> Contract:
        contract = Contract(
            account_id=account_id,
            kind=kind,
            rate=rate,
            principal_amount=principal_amount,
            maturity_date=maturity_date,
            compounding=compounding,
            payment_amount=payment_amount,
        )
        self.session.add(contract)
        await self.session.commit()
        await self.session.refresh(contract)
        return contract

    async def select_contract(self, contract_id: int) -> Contract | None:
        return await self.session.get(Contract, contract_id)

    async def select_contracts(self, account_id: Optional[int] = None) -> list[Contract]:
        stmt = select(Contract)
        if account_id is not None:
            stmt = stmt.where(Contract.account_id == account_id)
        return list(await self.session.scalars(stmt))

    async def update_contract(self, contract_id: int, **fields) -> Contract | None:
        contract = await self.session.get(Contract, contract_id)
        if contract is None:
            return None
        _apply_updates(contract, fields)
        await self.session.commit()
        await self.session.refresh(contract)
        return contract

    async def delete_contract(self, contract_id: int) -> bool:
        contract = await self.session.get(Contract, contract_id)
        if contract is None:
            return False
        await self.session.delete(contract)
        await self.session.commit()
        return True


class GoalRepository(BaseRepository):
    async def insert_goal(
        self,
        user_id: int,
        name: str,
        target_amount: Decimal,
        current_amount: Decimal,
        deadline: Optional[date] = None,
        account_id: Optional[int] = None,
    ) -> Goal:
        goal = Goal(
            user_id=user_id,
            name=name,
            target_amount=target_amount,
            current_amount=current_amount,
            deadline=deadline,
            account_id=account_id,
        )
        self.session.add(goal)
        await self.session.commit()
        await self.session.refresh(goal)
        return goal

    async def select_goal(self, goal_id: int) -> Goal | None:
        return await self.session.get(Goal, goal_id)

    async def select_goals(self, user_id: Optional[int] = None) -> list[Goal]:
        stmt = select(Goal)
        if user_id is not None:
            stmt = stmt.where(Goal.user_id == user_id)
        return list(await self.session.scalars(stmt))

    async def update_goal(self, goal_id: int, **fields) -> Goal | None:
        goal = await self.session.get(Goal, goal_id)
        if goal is None:
            return None
        _apply_updates(goal, fields)
        await self.session.commit()
        await self.session.refresh(goal)
        return goal

    async def delete_goal(self, goal_id: int) -> bool:
        goal = await self.session.get(Goal, goal_id)
        if goal is None:
            return False
        await self.session.delete(goal)
        await self.session.commit()
        return True