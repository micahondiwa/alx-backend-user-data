#!/usr/bin/env python3
"""filtered_logger module that implements data obfuscation"""
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Returns an obfuscated log message
    Args:
        fields: list of strings indicating fields to obfuscate
        redaction: what the field will be obfuscated to
        message: the log line to obfuscate
        separator: the character separating the fields
    """
    for field in fields:
        message = re.sub(
            field + "=.*?" + separator, field + "=" + redaction + separator, message
        )
    return message
