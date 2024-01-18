#!/usr/bin/env python3
"""Session Authentication Module"""
from uuid import uuid4
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """class to implement session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user with id user_id
        Args:
            user_id (str): user's user id
        Return:
            None is user_id is None or not a string
            Session ID in string format
        """
        session_id = str(uuid4())
        if user_id and isinstance(user_id, str):
            self.user_id_by_session_id[str(session_id)] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
         Returns a user ID based on a session ID
        Args:
            session_id (str): session ID
        Return:
            user id or None if session_id is None or not a string
        """
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return a user instance based on a cookie value
        Args:
            request : request object containing cookie
        Return:
            User instance
        """
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            return User.get(user_id)
        return None

    def destroy_session(self, request=None) -> bool:
        """
        Deletes a user session
        """
        if request:
            session_id_cookie = self.session_cookie(request)
            if session_id_cookie:
                user_id = self.user_id_for_session_id(session_id_cookie)
                if user_id:
                    del self.user_id_by_session_id[session_id_cookie]
                    return True
                return False
            return False
        return False
        