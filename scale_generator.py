# coding=utf-8
"""
Generate all possible scales with no more than 2 semitones in sequence.

We want to generate some scales.
The scales must cover a single octave, and they must satisfy the requirements:
-   No sequence of three notes can be semitones apart. (Two notes is fine,)

This is equivalent to the following:
-   Construct a sequence of numbers which sum to 12 (the number of semitones in
	an octave, where no two consecutive numbers are 1.
	-   These numbers would correspond to the intervals between consecutive
		notes.

"""

from midiutil.MidiFile3 import MIDIFile

from cwcx.Lists import *
from cwcx.IO import *

# Some Constants

# The notes in an octave
NOTES = ['R', '♭2', '2', '♭3', '3', '4', '♯4', '5', '♯5', '6', '♭7', '7']
OCTAVE = len(NOTES)

# We use this to denote a partition that cannot be completed
DEAD_END = -1


def partition_with_intervals(remaining_length, proper_partitions_only=False):
	"""
	Generates all possible partitions of a thing of length `remaining`.
	:param proper_partitions_only: If this is set to true, the trivial partition of an interval with itself will be excluded.
	:param remaining_length:
	"""

	# If we're done, we can stop here
	if remaining_length == 0:
		return []

	# If exactly 1 is remaining, we can only partition it if allowed.
	elif remaining_length == 1:
		if proper_partitions_only:
			return [[DEAD_END]]
		else:
			return [[1]]

	# If exactly 2 are remaining, there are a small number of possible
	# partitions.
	elif remaining_length == 2:
		if proper_partitions_only:
			return [[1, 1]]
		else:
			return [[1, 1], [2]]

	# If exactly 3 are remaining, there are a small number of possible
	# partitions.
	elif remaining_length == 3:
		if proper_partitions_only:
			return [[1, 1, 1], [1, 2], [2, 1]]
		else:
			return [[1, 1, 1], [1, 2], [2, 1], [3]]

	# By providing results for 0, 1, 2 and 3 remaining, we have our base cases,
	# and so have paths forward.

	# If more than 3 remain, we are in our recursion case, and we defer
	# partitioning to another function call.
	else:

		# The partition of this interval will be all possible interval choices
		# crossed by all possible partitions of the remaining part of the
		# octave.

		partition_list = []

		# We go through all possible intervals we are allowed to choose at this
		# stage.
		for chosen_interval in range(1, remaining_length + 1):

			# For each one of those intervals, the amount we have *left* to
			# partition is lessened by the interval we chose.
			left_to_partition = remaining_length - chosen_interval

			# It's the recursion step!
			partitions_of_remaining = partition_with_intervals(left_to_partition)

			# For each partition of the remaining, we prepend our chosen
			# interval, and add it to the list for this level.
			for partition in partitions_of_remaining:

				# Check for dead ends, and skip them if found
				if partition.__contains__(DEAD_END):
					continue

				else:
					# If we have a good partition, we add our interval to the
					# beginning.
					this_partition = [chosen_interval]
					this_partition.extend(partition.copy())

					# What we have now is *a valid partition of our specified
					# portion of an octave*.

					# So we add it to the list
					partition_list.append(this_partition)

		# Finally add the trivial partition
		if not proper_partitions_only:
			partition_list.append([remaining_length])

		# Now we have all possible partitions of our provided portion of the
		# octave, so we can return it to the next level up.
		return partition_list


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


def intervals_to_notes(intervals, start_with=0):
	"""
	Takes a list of intervals and produces a list of notes reached by following
	those intervals.
	:param intervals:
	:param start_with:
	"""

	# Start with the specified first note
	note_pointer = start_with
	note_list = [NOTES[note_pointer]]

	for interval in intervals:
		note_pointer += interval
		# Wrap around if we reach the end
		note_pointer %= OCTAVE
		note_list.append(NOTES[note_pointer])

	return note_list


def intervals_to_midifile(intervals, starting_note=69, tempo_bpm=120, track_name="track name"):
	"""
	Takes a list of intervals and prodces a midi file returning that scale.
	:param intervals:
	:param starting_note: 69 is middle A
	:param tempo_bpm:
	:param track_name:
	:return:
	"""
	current_note = starting_note
	midi_note_list = [current_note]
	for interval in intervals:
		current_note += interval
		midi_note_list.append(current_note)

	midi_file = MIDIFile(1)

	# constants
	track = 0
	channel = 0
	volume = 100
	timestep = 1
	note_duration = 1

	# initialise time
	time = 0

	midi_file.addTrackName(track, time, track_name)
	midi_file.addTempo(track, time, tempo_bpm)

	for note in midi_note_list:
		midi_file.addNote(track, channel, note, time, note_duration, volume)
		time += timestep

	return midi_file


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

	# Collects lists whichpass lenght requirements
	output_lists = []

	for input_list in input_lists:
		if (not filter_by_min_length) or (len(input_list) >= minimum):
			if (not filter_by_max_length) or (len(input_list) <= maximum):
				output_lists.append(input_list.copy())
	return output_lists


def display_scales(list_of_scales):
	"""
	Display and save to MIDI files.
	:param list_of_scales:
	:return:
	"""
	scale_number = 1
	for scale in list_of_scales:
		prints(scale_number, len(scale), scale, "\t\t", intervals_to_notes(scale))
		scale_number += 1


def save_scales(list_of_scales, save_path):
	"""
	Display and save to MIDI files.
	:param save_path:
	:param list_of_scales:
	:return:
	"""
	scale_number = 1
	for scale in list_of_scales:

		midi_file_name = os.path.join(save_path, "scale-{0}.mid".format(scale))
		midi_file = intervals_to_midifile(scale, track_name=midi_file_name)

		with open(midi_file_name, "wb") as opened_file:
			midi_file.writeFile(opened_file)

		scale_number += 1


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


def main():
	# TODO: Get this from passed arguments
	# Some constants
	save_path = '/Users/cai/Desktop/scales/'

	allow_chromatic_triplets = True
	allow_subscales = True
	allow_cyclic_permutations = True
	minimum_length = 0
	maximum_interval = 4

	# TODO: Nicer printed output.
	# TODO: Classification and naming of scales.

	# TODO: When removing sub-scales.  Am I checking against *all* scales, or just previous ones?

	# TODO: Log the removed scales at each stage, including reasons for removal.

	# First list all partitions of the octave, this is "all scales", but may have many repeats and have multiple
	# instances of things we don't want, such as chromatic triplets.
	list_of_scales = partition_with_intervals(OCTAVE)

	# Sort by length
	list_of_scales = sorted(list_of_scales, key=lambda l: len(l))

	if not allow_chromatic_triplets:
		list_of_scales = filter_by_chromatic_triples(list_of_scales)

	if not allow_cyclic_permutations:
		list_of_scales = filter_cyclic_permutations(list_of_scales)

	if not allow_subscales:
		list_of_scales = filter_subscales(list_of_scales)

	if minimum_length > 0:
		# TODO: this shouldn't be an optional argument
		list_of_scales = filter_by_length(list_of_scales, minimum=minimum_length)

	if maximum_interval > 0:
		list_of_scales = filter_by_maximum_interval(list_of_scales, maximum_permitted_interval=maximum_interval)

	# Display the list of scales
	display_scales(list_of_scales)

	#save_scales(list_of_scales, save_path)


def test():
	l = partition_with_intervals(4)
	display_scales(l)

if __name__ == "__main__":
	main()
