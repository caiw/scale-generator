# coding=utf-8
"""
Code relating to printing and displaying things in text.
"""

from datetime import datetime


# The notes in an octave
NOTES = ['R', 'm2', 'M2', 'm3', 'M3', 'M4', 's4', 'M5', 's5', 'M6', '♭7', 'M7']
OCTAVE = len(NOTES)


def prints(*args, sep=' ', end='\n', file=None):
	"""
	print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

	Prints the values to a stream, or to sys.stdout by default.

	Attaches a local timestamp to the start of the output.

	Optional keyword arguments:
	file:  a file-like object (stream); defaults to the current sys.stdout.
	sep:   string inserted between values, default a space.
	end:   string appended after the last value, default a newline.
	flush: whether to forcibly flush the stream.
	"""
	timestamp = "<{0}>".format(datetime.now())
	print(timestamp, *args, sep=sep, end=end, file=file)


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


def display_scales(list_of_scales):
	"""
	Display and save to MIDI files.
	:param list_of_scales:
	:return:
	"""
	scale_number = 1
	for scale in list_of_scales:
		prints(scale_number, '\t', len(scale), '\t', scale, "\t\t", intervals_to_notes(scale))
		scale_number += 1