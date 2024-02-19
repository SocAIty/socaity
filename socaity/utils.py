from enum import Enum
from typing import Union


def get_value_of_enum_or_default(enum: Enum, default_return=None) -> list:
    """
    Get the values of an Enum.
    :param enum: the Enum
    :return: a list of the values
    """


    return [e.value for e in enum]