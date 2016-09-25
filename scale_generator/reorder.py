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


def cyclic_permutations(input_list):
	"""
	Lists all cyclic permutations of a given list.
	:param input_list:
	:return:
	"""

	permutation_list = [input_list]

	permutation = input_list.copy()

	# can skip the last one because we've already got the identity permutation
	for perutation_i in range(len(input_list) - 1):
		permutation = cyclic_shift(permutation)
		permutation_list.append(permutation)

	return permutation_list
