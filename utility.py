
"""
utility.py:
Functions that do not directly impact bot commands go here
"""
from datetime import datetime, date, timedelta

def list2string(li):
    z = ""
    for item in li:
        z = z + item.mention + " "
    return z