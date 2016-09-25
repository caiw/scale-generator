# coding=utf-8
def partition_with_intervals(remaining_length, proper_partitions_only=False):
	"""
	Generates all possible partitions of a thing of length `remaining`.
	:param proper_partitions_only: If True, the trivial partition of an interval with itself will be excluded.
	:param remaining_length:
	"""

	# We use this to denote a partition that cannot be completed
	# noinspection PyPep8Naming
	DEAD_END = -1  # constants should be upper case!

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
