# coding=utf-8

"""
Errors.
"""

class ApplicationError(Exception):
    """
    Represents an error in which the executing code is in a logically invalid
    state. This means that a programmer error has occurred.
    :param value:
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidOperationError(Exception):
    """
    Represents an error in which the operation is invalid given the state of things.
    :param value:
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
