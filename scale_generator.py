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

from cw_common import *



## Some Connstants

# The number of semitones in an octave
OCTAVE = 12

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

    # If exactly 2 is remaining, there are a small number of possible
    # partitions.
    # By providing results for 0, 1 and 2 remaining, we have paths forward
    # whether or not an initial 1 is permitted.
    elif remaining == 2:
        if initial_one_allowed:
            return [[1,1], [2]]
        else:
            return [[2]]

    # If more than 2 remain, we are in our recursion case, and we defer
    # partitioning to another function call.
    else:

        if initial_one_allowed:
            start = 1
        else:
            start = 1

        # The partition of this interval will be all possible interval choices
        # crossed by all possible partitions of the remaining part of the
        # octave.

        interval_list = []

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
                    interval_list.append(this_partition)

        # Now we have all possible partitions of our provided portion of the
        # octave, so we can return it to the next level up.
        return interval_list



def main():

    list_of_partitions = partition_with_intervals(OCTAVE)
    scale_number = 1
    for partition in list_of_partitions:
        prints(scale_number, partition, sum(partition))
        scale_number += 1


if __name__ == "__main__":
    main()
