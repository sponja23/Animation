import numpy as np

def ensureArray(obj):
	if not isinstance(obj, np.ndarray):
		return np.array(obj)
	return obj

def ensureList(obj):
	if type(obj) is not list and type(obj) is not tuple:
		return list(obj)
	return obj