# coding=utf-8

"""
List utility functions.
"""

import cwcx.Errors as Errors


def check_for_consecutive_values(input_list, value_to_check):
	"""
	Checks a list to see if any pair of consecutive values are the same.
	Returns True if this is the case, else returns False.
	:param input_list:
	:param value_to_check:
	:return:
	"""
	for value_i in range(1,len(input_list)):
		previous_value = input_list[value_i-1]
		next_value = input_list[value_i]
		if previous_value == next_value:
			return True
	return False


def Nones(l):
    """
    Produces a list of None of the specified length l
    :param l:
    :return:
    """
    return repvect(l, None)


def zeros(l):
    """
    Produces a list of 0 of the specified length l
    :param l:
    :return:
    """
    return repvect(l, 0)


def repvect(l, v):
    """
    Produces a list of v of the specified length l
    :param v:
    :param l:
    :return:
    """
    return l * [v]


if __name__ == "__main__":
	raise Errors.InvalidOperationError("Don't run library code.")
