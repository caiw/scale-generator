# coding=utf-8
"""
Code related to reordering scales.
"""


def cyclic_shift(input_list, n=1):
	"""
	Applies a cyclic permutation to a list.
	:param input_list:
	:param n:
	:return:
	"""
	shifted_list = input_list[n:] + input_list[:n]
	return shifted_list


def cyclic_permutations(input_list, include_trivial=True):
	"""
	Lists all cyclic permutations of a given list.
	:param include_trivial: Include the trivial cyclic permutation (identity perm)?
	:param input_list:
	:return:
	"""

	if include_trivial:
		permutation_list = [input_list]
	else:
		permutation_list = []

	permutation = input_list.copy()

	# can skip the last one because we've already got the identity permutation if we want it
	for permutation_i in range(len(input_list) - 1):
		permutation = cyclic_shift(permutation)
		permutation_list.append(permutation)

	return permutation_list
