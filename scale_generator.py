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

import re

import scipy
import scipy.io

from midiutil.MidiFile3 import MIDIFile

from cw_common import *



## Some Connstants

# The notes in an octave
#NOTES = ['A', 'B♭', 'B', 'C', 'C♯', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭']
NOTES = ['R', '♭2', '2', '♭3', 'M3', '4', '♯4', '5', '♯5', '6', '♭7', 'M7']
OCTAVE = len(NOTES)

# We use this to denote a partition that cannot be completed
DEAD_END = -1

def partition_with_intervals(remaining, initial_one_allowed=True):

    # If we're done, we can stop here
    if remaining == 0:
        return []

    # If exactly 1 is remaining, we can only proceed if we're allowed to use
    # 1. Otherwise we can't proceed.
    elif remaining == 1:
        if initial_one_allowed:
            return [[1]]
        else:
            # Can use -1 as an error case
            return [[DEAD_END]]

    # If exactly 2 are remaining, there are a small number of possible
    # partitions.
    elif remaining == 2:
        return [[2]]

    # If exactly 3 are remaining, there are a small number of possible
    # partitions.
    elif remaining == 3:
        if initial_one_allowed:
            return [[1,2], [2,1], [3]]
        else:
            return [[2,1], [3]]


    # By providing results for 0, 1, 2 and 3 remaining, we have paths forward
    # whether or not an initial 1 is permitted.

    # If more than 2 remain, we are in our recursion case, and we defer
    # partitioning to another function call.
    else:

        if initial_one_allowed:
            start = 1
        else:
            start = 2

        # The partition of this interval will be all possible interval choices
        # crossed by all possible partitions of the remaining part of the
        # octave.

        partition_list = []

        # We go through all possible intervals we are allowed to choose at this
        # stage.
        for chosen_interval in range(start, remaining + 1):

            # For each one of those intervals, the amount we have *left* to
            # partition is lessened by the interval we chose.
            left_to_partition = remaining - chosen_interval

            # We are only allowed a one as the *next* choice, if we didn't just
            # p.ick it
            one_allowed_as_next_interval = chosen_interval != 1

            # It's the recursion step!
            partitions_of_remaining = partition_with_intervals(left_to_partition, one_allowed_as_next_interval)

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
        partition_list.append([remaining])

        # Now we have all possible partitions of our provided portion of the
        # octave, so we can return it to the next level up.
        return partition_list

def intervals_to_notes(intervals, start_with=0):
    """
    Takes a list of intervals and produces a list of notes reached by following
    those intervals.
    """

    # Start with the specified first note
    note_pointer = start_with
    note_list = [NOTES[note_pointer]]

    for interval in intervals:
        note_pointer += interval
        note_pointer %= OCTAVE
        note_list.append(NOTES[note_pointer])

    return note_list

def intervals_to_midifile(intervals, starting_note=69, tempo_bpm=120, track_name="track name"): #69 is middle A??
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


def main(no_fewer_than=7, save_files=False):
    # TODO: We're not discarding those which are cyclic permutations of others

    list_of_partitions = partition_with_intervals(OCTAVE)
    scale_number = 1
    for partition in list_of_partitions:
        # Only interested in scales with at least 7 notes.
        if len(partition) < no_fewer_than:
            continue

        #todo should discard some if it's the same as an existing one but with a note removed

        prints(scale_number, partition, intervals_to_notes(partition))

        midi_file_name = "scale-{0}.mid".format(scale_number)
        midi_file = intervals_to_midifile(partition)

        with open(midi_file_name, "wb") as opened_file:
            midi_file.writeFile(opened_file)

        scale_number += 1

if __name__ == "__main__":
    main(
        save_files=False,
        no_fewer_than=6
    )
