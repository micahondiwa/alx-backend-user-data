#!/usr/bin/env python3
"""
Main file
"""
from user import User

print(User.__tablename__)

for column in User.__tablename__.columns:
    print("{}: {}".format(column, column.type))
