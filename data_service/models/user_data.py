from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, date
from core.database import Base
from decimal import Decimal
from typing import Optional
from contracts.transaction import TransactionCategory
import enum
import uuid

from sqlalchemy import (
    BigInteger,
    String,
    Numeric,
    DateTime,
    Date,
    Uuid,
    ForeignKey,
)

class AccountType(enum.Enum):
    DEPOSIT = "deposit"
    CHECKING = "checking"
    LOAN = "loan"

class ContractKind(enum.Enum):
    ACCRUAL = "accrual"
    AMORTIZING = "amortizing"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    uuid: Mapped[uuid.UUID] = mapped_column(Uuid, unique=True)

    accounts = relationship("Account", cascade="all, delete-orphan", passive_deletes=True)
    transactions = relationship("Transaction", cascade="all, delete-orphan", passive_deletes=True)
    goals = relationship("Goal", cascade="all, delete-orphan", passive_deletes=True)


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String)
    type: Mapped[AccountType]
    balance: Mapped[Decimal] = mapped_column(Numeric)

    transactions = relationship("Transaction", cascade="all, delete-orphan", passive_deletes=True)
    contracts = relationship("Contract", cascade="all, delete-orphan", passive_deletes=True)


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    account_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("accounts.id", ondelete="CASCADE"))
    amount: Mapped[Decimal] = mapped_column(Numeric)
    ts: Mapped[datetime] = mapped_column(DateTime)
    balance: Mapped[Decimal] = mapped_column(Numeric)
    category: Mapped[TransactionCategory]
    goal_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("goals.id", ondelete="SET NULL"))
    goal = relationship("Goal", back_populates="transactions")

class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    account_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("accounts.id", ondelete="CASCADE"))
    kind: Mapped[ContractKind]
    rate: Mapped[Decimal] = mapped_column(Numeric)
    principal_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    maturity_date: Mapped[Optional[date]] = mapped_column(Date)
    compounding: Mapped[Optional[str]] = mapped_column(String)
    payment_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric)


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String)
    target_amount: Mapped[Decimal] = mapped_column(Numeric)
    current_amount: Mapped[Decimal] = mapped_column(Numeric)
    deadline: Mapped[Optional[date]] = mapped_column(Date)
    account_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("accounts.id", ondelete="CASCADE"))
    transactions = relationship("Transaction", back_populates="goal", passive_deletes=True)
