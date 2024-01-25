#!/usr/bin/env python3
"""DB Module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite://a.db", echo=True)
        Base.medatada.drop_all(self._engine)
        Base.medatada.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the db
        Args:
        email(str): The email address of the user
        hashed_password(str): User password
        Returns:
        user: Newly created user
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kargs) -> User:
        """
        Finds a user by the given criteria
        Args:
        **kargs: The search criteria
        Returns:
        User: The user found
        """
        all_users = self.session.query(User)
        for k, v in kargs.items():
            if k not in User.__dict__:
                raise InvalidRequestError
            for user in all_users:
                if getattr(user, k) == v:
                    return user
        return NoResultFound
