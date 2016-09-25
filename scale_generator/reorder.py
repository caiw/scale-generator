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


def cyclic_permutations(scale, include_trivial=True):
	"""
	Lists all cyclic permutations of a given list.
	Only returns unique permutations.
	Order not guaranteed.
	:param include_trivial: Include the trivial cyclic permutation (identity perm)?
	:param scale:
	:return:
	"""

	if include_trivial:
		permutation_list = [scale]
	else:
		permutation_list = []

	permutation = scale.copy()

	# can skip the last one because we've already got the identity permutation if we want it
	for permutation_i in range(len(scale) - 1):
		permutation = cyclic_shift(permutation)
		permutation_list.append(permutation)

	# In some cases, e.g. with [6,6], even if we specify no trivial, we get it anyway (as it's also a nontrivial
	# permutation, before uniqueness checking). So we have to remove it manually.
	if not include_trivial and scale in permutation_list:
		permutation_list.remove(scale)

	# finally, in case all cyclic permutations produce duplicates (e.g. of [1,1,1,1]), we only return unique entries
	unique_permutation_list = [list(u_perm) for u_perm in set(tuple(perm) for perm in permutation_list)]

	return unique_permutation_list
