# coding=utf-8


def contains_sublist(superlist, sublist):
	"""
	http://stackoverflow.com/a/3314913/2883198
	:param superlist:
	:param sublist:
	:return:
	"""
	n = len(sublist)
	return any((sublist == superlist[i:i + n]) for i in range(len(superlist) - n + 1))
