import re

# Token Format
TYPE_WILD = "*"  # *
TYPE_STEPS = "*/x"  # */num
TYPE_RANGE = "n-n"  # num - num  , range type
TYPE_SPLITS = "n,n"  # num,num
TYPE_NUMBER = "n"  # num

MINUTE = "MINUTE"
HOUR = "HOUR"
MONTH = "MONTH"
DAY_OF_MONTH = "DAY OF MONTH"
DAY_OF_WEEK = "DAY OF WEEK"

REG_EXP = {
    TYPE_WILD: r"^\*$",
    TYPE_STEPS: r"^\*\/[0-9]+$",
    TYPE_RANGE: r"^[0-9]+\-[0-9]+",
    TYPE_NUMBER: r"^[0-9]+$",
    TYPE_SPLITS: r"^([0-9]+\,)+[0-9]+$"
}

# 0th arg mapping
TIME_VALUES = {
    0: [MINUTE, 0, 59],  # [typename, start , end]
    1: [HOUR, 0, 23],  # HOUR
    3: [MONTH, 1, 12],  # MONTH
    2: [DAY_OF_MONTH, 1, 31],
    4: [DAY_OF_WEEK, 1, 7]  # DAY OF WEEK
}

MONTHDAYS = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def get_time_name(time_index):
    return TIME_VALUES[time_index][0]


def get_start_end(time_index):
    return TIME_VALUES[time_index][1], TIME_VALUES[time_index][2]


def is_valid_number(number, time_index):
    start = TIME_VALUES[time_index][1]
    end = TIME_VALUES[time_index][2]
    if start <= int(number) <= end:
        return True
    return False


def is_valid_day(day, month):
    if day <= MONTHDAYS[month]:
        return True
    return False


def validate_tokens(value=""):
    for format_type, reg in REG_EXP.iteritems():
        if re.match(reg, value):
            return bool(re.match(reg, value)), format_type
    return False, None
