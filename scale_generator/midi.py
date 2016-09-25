# coding=utf-8
"""
Code relating to creation of MIDI files.
"""

import os

from midiutil.MidiFile3 import MIDIFile


def save_scales_as_midi(list_of_scales, save_path):
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
