#!/usr/bin/env python3
"""basic_auth module"""
import re
import binascii
from base64 import b64decode
from typing import TypeVar, Tuple, Union
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Class to implement basic authentication
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> Union[str, None]:
        """
        Return:
            - Base64 part of the Authorization header for basic authentication
        """
        if authorization_header:
            if type(authorization_header) is not str:
                return None
            pattern = r"Basic (?P<token>.+)"
            if re.fullmatch(pattern, authorization_header.strip()):
                return re.fullmatch(pattern, authorization_header
                                    .strip()).group(
                    "token"
                )
            return None
        return None

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> Union[str, None]:
        """
        Return:
            - Decoded value of a Base64 string base64_authorization_header
        """
        if base64_authorization_header:
            if type(base64_authorization_header) is not str:
                return None
            try:
                res = b64decode(base64_authorization_header, validate=True)
                return res.decode("utf-8")
            except (binascii.Error, UnicodeDecodeError):
                return None
        return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[Union[str, None], Union[str, None]]:
        """
        Return:
            - user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header:
            if type(decoded_base64_authorization_header) is not str:
                return None, None
            if ":" in decoded_base64_authorization_header:
                email = decoded_base64_authorization_header.split(":")[0]
                password = decoded_base64_authorization_header
                [len(email) + 1:]
                return email, password
            return None, None
        return None, None

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> Union[TypeVar("User"), None]:
        """
        Return:
            - User instance based on his email and password
        """
        if type(user_email) is str and type(user_pwd) is str:
            try:
                users = User.search({"email": user_email})
                if not users or users == []:
                    return None
                for user in users:
                    if user.is_valid_password(user_pwd):
                        return user
                return None
            except Exception:
                return None
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        if auth_header:
            token = self.extract_base64_authorization_header(auth_header)
            if token:
                decoded = self.decode_base64_authorization_header(token)
                if decoded:
                    email, passwd = self.extract_user_credentials(decoded)
                    if email and passwd:
                        return self.user_object_from_credentials(email, passwd)
        return
