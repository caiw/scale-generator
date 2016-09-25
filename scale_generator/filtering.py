# coding=utf-8
"""
Code for filtering lists of scales.
"""

from scale_generator.lists import *
from scale_generator.reorder import *
from scale_generator.printing import *


def filter_by_chromatic_triples(list_of_scales, verbose=False):
	"""
	Removes scales from a list if they contain chromatic triplets.
	:param verbose:
	:param list_of_scales:
	:return:
	"""

	if verbose:
		prints()
		prints("Filtering scales based on presence of chromatic triplets...")

	accepted_list = []
	for scale in list_of_scales:
		if contains_chromatic_triplets(scale):
			if verbose:
				prints("Removed {0} because it contains a chromatic triplet.".format(scale_to_interval_list_str(scale)))
		else:
			accepted_list.append(scale.copy())
	return accepted_list


def filter_by_maximum_interval(list_of_scales, max_permitted_interval, verbose=False):
	"""
	Filters a list by the largest size of interval.
	:param list_of_scales:
	:param max_permitted_interval:
	:param verbose:
	:return:
	"""

	if verbose:
		prints()
		prints("Filtering scales based on a maximum interval size of {0}...".format(max_permitted_interval))

	accepted_list = []
	for scale in list_of_scales:
		scale_ok = True
		offending_interval = None
		for interval in scale:
			if interval > max_permitted_interval:
				scale_ok = False
				offending_interval = interval
				break
		if scale_ok:
			accepted_list.append(scale.copy())
		else:
			if verbose:
				prints("Removed {0} because it contains an interval larger than {1} ({2}).".format(
					scale_to_interval_list_str(scale),
					max_permitted_interval,
					offending_interval))
	return accepted_list


def filter_subscales(input_scales, verbose=False):
	"""
	Remove scales from a list if they are the same as existing scales with some
	notes removed.
	:param verbose:
	:param input_scales:
	:return:
	"""

	if verbose:
		prints()
		prints("Filtering scales based on the presence of refinements...")

	# Collect scales which pass the test
	filtered_list = []

	for scale in input_scales:

		# List of possible refinements of this scale
		refinements = scale_refinements(scale)

		# Record the contaminating refinement
		contaminating_refinement = None

		# For each refinement of the current scale, we'll go through the
		# other scales in the list, ...
		this_scale_is_clean = True
		for refinement in refinements:
			# ... and if one of the refinements already exists, ...
			if refinement in input_scales:
				# ... we mark this scale as tainted
				this_scale_is_clean = False
				contaminating_refinement = refinement
				break
		# ... and only if it isn't tainted after we've considered all
		# refinements will we add it to our list.
		if this_scale_is_clean:
			filtered_list.append(scale.copy())
		else:
			if verbose:
				prints("Removed {0} because it is a subscale of {1}.".format(
					scale_to_interval_list_str(scale),
					scale_to_interval_list_str(contaminating_refinement)))
	return filtered_list


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


def filter_modes(input_scales, verbose=False):
	"""
	From a list of scales, removes any member which is a mode (cyclic permutation) of another member.
	:param verbose:
	:param input_scales:
	:return:
	"""

	if verbose:
		prints()
		prints("Filtering scales based on the presence of other modes...")

	# To collect the lists which pass the test
	# We add the first one, no questions asked.
	accepted_scales = [input_scales[0]]

	# All after the first will get checked.
	for scale in input_scales[1:]:

		# Record the scale which may cause this one to be rejected as a mode
		offending_root = None

		is_new = True
		for accepted_scale in accepted_scales:
			modes = cyclic_permutations(accepted_scale)
			if scale in modes:
				is_new = False
				offending_root = accepted_scale
				break

		if is_new:
			accepted_scales.append(scale)
		else:
			if verbose:
				prints("Removed {0} because it is a mode of {1}.".format(
					scale_to_interval_list_str(scale),
					scale_to_interval_list_str(offending_root)))

	return accepted_scales


def filter_by_length(input_scales, minimum=-1, maximum=-1, verbose=False):
	"""
	Filters a list of lists by their length.
	:param verbose:
	:param input_scales:
	:param minimum:
	:param maximum:
	:return:
	"""

	if verbose:
		prints()
		prints("Filtering scales based on length...")

	# Check whether to do min/max filtering
	filter_by_min_length = (minimum >= 0)
	filter_by_max_length = (maximum >= 0)

	# Collects lists which pass length requirements
	output_lists = []

	for scale in input_scales:
		if (not filter_by_min_length) or (len(scale) >= minimum):
			if (not filter_by_max_length) or (len(scale) <= maximum):
				output_lists.append(scale.copy())
			else:
				if verbose:
					prints("Removed {0} because its length was out of bounds.".format(
						scale_to_interval_list_str(scale)))
	return output_lists
