from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Enum
from typing import Optional
from . import db


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    name: Mapped[str] = mapped_column(String(1000))
    password: Mapped[str] = mapped_column(String(1000))
    confirmation_code: Mapped[str] = mapped_column(String(6))
    confirmed: Mapped[bool] = mapped_column(Boolean())
    

class Gift(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    gifter: Mapped[int] = mapped_column(Integer(), nullable=False)
    giftee: Mapped[int] = mapped_column(Integer(), nullable=False)
    gift: Mapped[str] = mapped_column(String(100), nullable=False)
    details: Mapped[Optional[str]] = mapped_column(String(1000))
    price: Mapped[int] = mapped_column(Integer())
    link: Mapped[Optional[str]] = mapped_column(String(1000))


class Friend(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    uid1: Mapped[int] = mapped_column(Integer(), nullable=False)
    uid2: Mapped[int] = mapped_column(Integer(), nullable=False)
    requestor: Mapped[str] = mapped_column(Enum('UID1', 'UID2'), nullable=False)


class FriendRequest(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    friend_id: Mapped[int] = mapped_column(Integer(), nullable=False)


