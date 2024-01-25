#!/usr/bin/env python3
"""
the auth module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import union
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes a password string and returns bytes
    Args:
    password (str): password in string format
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
