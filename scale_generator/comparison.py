# coding=utf-8
"""
Code related to comparing scales.
"""

from scale_generator.reorder import *


def contains_cumulative_interval(scale, interval_size):
	"""
	Returns true if a scale contains a particular interval.
	:param interval_size:
	:param scale:
	:return:
	"""

	# This basically amounts to playing blackjack:
	# we add up intervals starting from the first, and if we hit the interval size before we exceed it, we win.
	total = 0
	for interval in scale:
		total += interval
		if total == interval_size:
			return True
		elif total > interval_size:
			return False
	# We shouldn't really get here
	return False


def contains_major_third(scale):
	"""
	Returns true if a scale contains a major third.
	:param scale:
	:return:
	"""

	# A major third is 4 semitones.
	MAJOR_THIRD = 4

	return contains_cumulative_interval(scale, MAJOR_THIRD)


def contains_major_seventh(scale):
	"""
	Returns true if a scale contains a major seventh.
	:param scale:
	:return:
	"""

	# A major seventh is 11 semitones.
	MAJOR_SEVENTH = 11

	return contains_cumulative_interval(scale, MAJOR_SEVENTH)


def contains_perfect_fifth(scale):
	"""
	Returns true if a scale contains a perfect fifth.
	:param scale:
	:return:
	"""

	# A perfect fifth is 7 semitones.
	PERFECT_FIFTH = 7

	return contains_cumulative_interval(scale, PERFECT_FIFTH)


def contains_flat_seveth(scale):
	"""
	Returns true if a scale contains a flat seventh.
	:param scale:
	:return:
	"""

	# A flat seventh is 10 semitones.
	FLAT_SEVENTH = 10

	return contains_cumulative_interval(scale, FLAT_SEVENTH)


def scale_distance(scale, target_scale):
	"""
	The distance between a scale and target scale.
	:param scale:
	:param target_scale:
	:return:
	"""
	pass


def majority_score(scale):
	"""
	Give a scale a score based on how major it is.
	:param scale:
	:return:
	"""

	# Here we're scoring by how close something is to a major scale by whether or not it satisfies these conditions, in
	# this order:

	# 1. Contains a major third
	# 2. Contains a major seventh
	# 3. Contains a perfect fifth
	# 4. Doesn't contain a flat seventh

	score = 0
	if contains_major_third(scale):
		score += 8
	if contains_major_seventh(scale):
		score += 4
	if contains_perfect_fifth(scale):
		score += 2
	if not contains_flat_seveth(scale):
		score += 1

	return score


def most_major_mode(scale):
	"""
	Return the most major mode of a scale.
	:param scale:
	:return:
	"""

	# If more than one scales satisfy the same score, we just pick one at random

	modes = cyclic_permutations(scale)

	m_m_m = None
	best_score = 0
	for mode in modes:
		mode_score = majority_score(mode)
		if mode_score > best_score:
			best_score = mode_score
			m_m_m = mode.copy()

	return m_m_m
