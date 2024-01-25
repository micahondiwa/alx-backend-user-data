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


def _generate_uuid() -> str:
    """
    Generates a uuid and return its string rep
    """
    return str(uuid4())


class Auth:
    """Auth class iteracts with the authentication db"""

    def __init__(self):
        self.__db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user and return a user object
        Args:
            email (str): new user's email address
            password (str): new users password
        Returns:
            if no user with given email exists, return newly created user
            else raise ValueError
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            password = _hash_password(password)
            user = self._db.add_user(email, password)
            return user
        raise ValueError(f'User {email} already exists')
    
    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials and return True is they are 
        correct or false if they are not.
        Args:
            email (str): user's email address
            password(str): user's password
        Return:
            True is credentials are correct, else false.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) ->Union[str, None]:
        """
        creates session_id for an existing user and update the 
        user's session_id attribute.
        Args:
            email(str): user's email address
        Return:
            session_id
        """
        try: 
            user = self._db.find_user_by(email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id=session_id: str) -> Union[User, None]:
        """
        Takes a session_id and returns the corresponding user, if one exists,
        else returns None.
        Args: 
            session_id (str): session id for user
        Return:
            user object if found, else None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Takes a user_id and destroy that user's session and update their
        session_id attribute to None.
        Args:
            user_id(int): user's id
        Return:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None 
        self._db.update_user(user.id, session_id=None)
    
    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset_token uuid for a user identified by the given email
        Args:
            email (str): user's email address.
        Return:
            newly generated reset_token for the relevant user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self.__db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_passsword(self, reset_token: str, password: str) -> None:
        """
        updates a user's password
        Args:
            reset_token(str): reset_token issued to reset the password
            password(str): user's new password
        Return:
            None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        new_pass = _hash_password(password)
        self._db.update_user(user.id, hashed_password=new_pass,
                            reset_token=None)
                            