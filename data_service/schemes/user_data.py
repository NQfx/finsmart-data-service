import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from contracts.transaction import TransactionCategory
from models.user_data import AccountType, ContractKind


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserOut(ORMBase):
    uuid: uuid.UUID


class AccountCreate(BaseModel):
    name: str
    type: AccountType
    balance: Decimal


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[AccountType] = None
    balance: Optional[Decimal] = None


class AccountOut(ORMBase):
    id: int
    name: str
    type: AccountType
    balance: Decimal


class TransactionCreate(BaseModel):
    amount: Decimal
    user_id: int
    ts: datetime
    balance: Decimal
    category: TransactionCategory
    account_id: Optional[int] = None
    goal_id: Optional[int] = None


class TransactionUpdate(BaseModel):
    account_id: Optional[int] = None
    user_id: Optional[int] = None
    amount: Optional[Decimal] = None
    ts: Optional[datetime] = None
    balance: Optional[Decimal] = None
    category: Optional[TransactionCategory] = None
    goal_id: Optional[int] = None


class TransactionOut(ORMBase):
    id: int
    account_id: Optional[int]
    amount: Decimal
    ts: datetime
    balance: Decimal
    category: TransactionCategory
    goal_id: Optional[int]


class ContractCreate(BaseModel):
    account_id: int
    kind: ContractKind
    rate: Decimal
    principal_amount: Optional[Decimal] = None
    maturity_date: Optional[date] = None
    compounding: Optional[str] = None
    payment_amount: Optional[Decimal] = None


class ContractUpdate(BaseModel):
    account_id: Optional[int]
    kind: Optional[ContractKind] = None
    rate: Optional[Decimal] = None
    principal_amount: Optional[Decimal] = None
    maturity_date: Optional[date] = None
    compounding: Optional[str] = None
    payment_amount: Optional[Decimal] = None


class ContractOut(ORMBase):
    id: int
    account_id: int
    kind: ContractKind
    rate: Decimal
    principal_amount: Optional[Decimal]
    maturity_date: Optional[date]
    compounding: Optional[str]
    payment_amount: Optional[Decimal]


class GoalCreate(BaseModel):
    name: str
    target_amount: Decimal
    current_amount: Decimal = Decimal("0")
    deadline: Optional[date] = None
    account_id: Optional[int] = None


class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[Decimal] = None
    current_amount: Optional[Decimal] = None
    deadline: Optional[date] = None
    account_id: Optional[int] = None


class GoalOut(ORMBase):
    id: int
    name: str
    target_amount: Decimal
    current_amount: Decimal
    deadline: Optional[date]
    account_id: Optional[int]