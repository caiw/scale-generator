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


from scale_generator.filtering import *
from scale_generator.printing import *
from scale_generator.midi import *


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
