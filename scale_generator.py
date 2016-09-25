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

import argparse

from scale_generator.filtering import *
from scale_generator.printing import *
from scale_generator.midi import *


def main():

	# Parse command line args
	parser = argparse.ArgumentParser()

	parser.add_argument(
		"--save_midi_to",
		help="The path to save midi files to.")
	parser.add_argument(
		"--filter_modes",
		help="Filter out different modes (cyclic permutations) of scales in the list.",
		action="store_true")
	parser.add_argument(
		"--filter_chromatic_triplets",
		help="Filter out scales featuring chromatic triplets.",
		action="store_true")
	parser.add_argument(
		"--filter_subscales",
		help="Filter out scales which are the same as others, with notes removed.",
		action="store_true")
	parser.add_argument(
		"--max_interval",
		help="The largest permitted interval between two notes, in semitones.",
		type=int)
	parser.add_argument(
		"--min_length",
		help="The shortest permitted length of scale.",
		type=int)

	args = parser.parse_args()

	# TODO: Nicer printed output.
	# TODO: Classification and naming of scales.

	# TODO: When removing sub-scales.  Am I checking against *all* scales, or just previous ones?

	# TODO: Log the removed scales at each stage, including reasons for removal.

	# First list all partitions of the octave, this is "all scales", but may have many repeats and have multiple
	# instances of things we don't want, such as chromatic triplets.
	list_of_scales = partition_with_intervals(OCTAVE)

	# Sort by length
	list_of_scales = sorted(list_of_scales, key=lambda l: len(l))

	if args.filter_chromatic_triplets:
		list_of_scales = filter_by_chromatic_triples(list_of_scales)

	if args.filter_modes:
		list_of_scales = filter_cyclic_permutations(list_of_scales)

	if args.filter_subscales:
		list_of_scales = filter_subscales(list_of_scales)

	if args.max_interval and args.max_interval > 0:
		list_of_scales = filter_by_maximum_interval(list_of_scales, maximum_permitted_interval=args.max_interval)

	if args.min_length and args.min_length > 0:
		# TODO: this shouldn't be an optional argument
		list_of_scales = filter_by_length(list_of_scales, minimum=args.min_length)

	if args.save_midi_to:
		save_scales_as_midi(list_of_scales, args.save_midi_to)

	# Display the list of scales
	display_scales(list_of_scales)


if __name__ == "__main__":
	main()
