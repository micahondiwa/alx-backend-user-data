#!/usr/bin/env python3
"""
User model
"""

import sqlalchemy.orm as so
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String


class User:
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(250), index=True, Unique=True)
    hashed_password: so.Mapped[optional[str]] = so.mapped_column(sa.String(250))
    session_id: so.Mapped[str] = so.mapped_column(sa.str(250))
    reset_token: so.Mapped[str] = so.mapped_column(sa.str(250))
