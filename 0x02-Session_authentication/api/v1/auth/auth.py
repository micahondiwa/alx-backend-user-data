#!/usr/bin/env python3
"""module with class to manage the API authentication"""
from typing import List, TypeVar, Union
import re


class Auth:
    """class to manage authentication of the API"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication or not
        Args:
            - path(str): Url path to be checked
            - excluded_paths(List of str): List of paths that do not require
              authentication
        Return:
            - True if path is not in excluded_paths, else False
        """
        if path is not None and excluded_paths is not None:
            for exclude in [pat.strip() for pat in excluded_paths]:
                pattern = ""
                if exclude[-1] == "*":
                    pattern = "{}.*".format(exclude[0:-1])
                elif exclude[-1] == "/":
                    pattern = "{}/*".format(exclude[0:-1])
                else:
                    pattern = "{}/*".format(exclude)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> Union[str, None]:
        """
        Returns the authorization header from a request object
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> Union[TypeVar("User"), None]:
        """
        Returns a User instance from information from a request object
        """
        return None
