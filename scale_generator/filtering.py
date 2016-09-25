# coding=utf-8
"""
Code for filtering lists of scales.
"""

from scale_generator.partition import *
from scale_generator.lists import *


def filter_by_chromatic_triples(list_of_scales):
	"""
	Removes scales from a list if they contain chromatic triplets.
	:param list_of_scales:
	:return:
	"""
	accepted_list = []
	for scale in list_of_scales:
		if not contains_chromatic_triplets(scale):
			accepted_list.append(scale.copy())
	return accepted_list


def filter_by_maximum_interval(list_of_scales, maximum_permitted_interval):
	accepted_list = []
	for scale in list_of_scales:
		scale_ok = True
		for interval in scale:
			if interval > maximum_permitted_interval:
				scale_ok = False
				break
		if scale_ok:
			accepted_list.append(scale.copy())
	return accepted_list


def filter_subscales(input_scales):
	"""
	Remove scales from a list if they are the same as existing scales with some
	notes removed.
	:param input_scales:
	:return:
	"""

	# Collect scales which pass the test
	filtered_list = []

	for scale in input_scales:

		# List of possible refinements of this scale
		refinements = scale_refinements(scale)

		# For each refinement of the current scale, we'll go through the
		# other scales in the list, ...
		this_scale_is_clean = True
		for refinement in refinements:
			# ... and if one of the refinements already exists, ...
			if refinement in input_scales:
				# ... we mark this scale as tainted
				this_scale_is_clean = False
				break
		# ... and only if it isn't tainted after we've considered all
		# refinements will we add it to our list.
		if this_scale_is_clean:
			filtered_list.append(scale.copy())
	return filtered_list


def scale_refinements(input_scale):
	"""
	For a given scale (list of intervals), this will return a list of scales
	which can be found by sub-partitioning an inverval.
	:param input_scale:
	:return:
	"""

	# The list of refinements of the current scale
	subscale_list = []

	# We're using the interval index here as the loop variable, rather than the
	# interval itself, as we'll use it for slicing later.
	for interval_i in range(len(input_scale)):
		this_interval = input_scale[interval_i]

		# We know we can't sub-partition a semitone.
		if this_interval <= 1:
			continue

		# So we look at partitioning intervals greater than whole tones.
		else:
			# We want to exclude trivial sub-partitions
			sub_partitions = partition_with_intervals(this_interval, proper_partitions_only=True)

			# For each sub-partition, we see what that would look like grafted
			# into the whole scale.
			for sub_partition in sub_partitions:
				grafted_scale = input_scale[:interval_i] + sub_partition + input_scale[interval_i+1:]

				# And if this new scale passes the test, we add it to the list.
				subscale_list.append(grafted_scale.copy())

	return subscale_list


def contains_chromatic_triplets(input_scale):
	"""
	Returns true if the input scale (list of intervals) contains a chromatic
	triplet.
	:param input_scale:
	:return:
	"""
	# Don't want a pair of 1s anywhere in the list
	if contains_sublist(input_scale, [1, 1]):
		return True
	# This includes wrapping through the end, so we shift it once and check again
	elif contains_sublist(cyclic_shift(input_scale), [1, 1]):
		return True
	else:
		return False


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


def filter_cyclic_permutations(input_lists):
	"""
	From a list of lists, removes any member which is a cyclic permutation of
	another member.
	:param input_lists:
	:return:
	"""

	# To collect the lists which pass the test
	# We add the first one, no questions asked.
	filtered_list = [input_lists[0]]

	# All after the first will get checked.
	for input_list in input_lists[1:]:

		is_new = True
		for current_list in filtered_list:
			cyclic_perms = cyclic_permutations(current_list)
			if input_list in cyclic_perms:
				is_new = False
				break

		if is_new:
			filtered_list.append(input_list)

	return filtered_list


def filter_by_length(input_lists, minimum=-1, maximum=-1):
	"""
	Filters a list of lists by their length.
	:param input_lists:
	:param minimum:
	:param maximum:
	:return:
	"""
	filter_by_min_length = (minimum >= 0)
	filter_by_max_length = (maximum >= 0)

	# Collects lists which pass length requirements
	output_lists = []

	for input_list in input_lists:
		if (not filter_by_min_length) or (len(input_list) >= minimum):
			if (not filter_by_max_length) or (len(input_list) <= maximum):
				output_lists.append(input_list.copy())
	return output_lists
