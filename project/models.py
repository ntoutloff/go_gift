from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer
from typing import Optional
from . import db

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#     name = db.Column(db.String(1000))

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True) # primary keys are required by SQLAlchemy
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password = mapped_column(String(1000))
    name = mapped_column(String(1000))

class Gift(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    gifter: Mapped[int] = mapped_column(Integer(), nullable=False)
    giftee: Mapped[int] = mapped_column(Integer(), nullable=False)
    gift: Mapped[str] = mapped_column(String(100), nullable=False)
    details: Mapped[Optional[str]] = mapped_column(String(1000))
    price: Mapped[int] = mapped_column(Integer())
    link: Mapped[Optional[str]] = mapped_column(String(1000))
