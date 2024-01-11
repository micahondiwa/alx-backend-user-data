#!/usr/bin/env python3
"""
encrypt_password module implementing password hashing
and validation
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    returns a salted, hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validates if the provided password matches the hashed password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
