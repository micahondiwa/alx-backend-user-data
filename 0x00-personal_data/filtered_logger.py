#!/usr/bin/env python3
"""
Module for filtered_logger
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates the log message.
    """
    return re.sub(r"(?<=(" + "|".join(fields) + r")=)[^;]+", redaction, message)
