class Segmenter(object):
	def __init__(self, begin, eind, step):
		self.begin = begin
		self.eind = eind
		self.step = step

	def segment(self, item):
		rnge = range(self.begin, self.eind, self.step)
		if item > self.eind:
			return '%s-' % (rnge[-1],)
		elif item < self.begin:
			return '-%s' % (rnge[0],)
		else:
			i = 0
			while item > rnge[i]:
				i += 1
	 		return '%s-%s' % (rnge[i-1], rnge[i])

	def __call__(self, item):
		return self.segment(item)
