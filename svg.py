
class Circle:
	def __init__(self, cx, cy, r):
		self.cx = cx
		self.cy = cy
		self.r = r
		self.text = ''

	def asXML(self):
		return '<circle cx="%d" cy="%d" r="%d" style="%s">%s</circle>' % (
			self.cx, self.cy, self.r, 'fill-opacity:1;stroke:#000000;fill:#bfbfbf', self.text)

class Line:
	def __init__(self, x1, y1, x2, y2):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2

	def asXML(self):
		return '<line x1="%d" y1="%d" x2="%d" y2="%d" style="%s"/>' % (
			self.x1, self.y1, self.x2, self.y2,
			"stroke:#000000")

class Text:
	def __init__(self, x, y, text, size, style=''):
		self.text = text
		self.x = x - 15/2
		self.y = y + 15/2
		self.size = size
		self.style = style

	def asXML(self):
		return '<text x="%f" y="%f" style="%s">%s</text>' % (
			self.x, self.y, 'font-size:%spt;font-weight:bold;fill:#3333dd;%s' % (self.size, self.style),
			self.text)

class SVG:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.items = []

	def asXML(self):
		head = '<svg width="%d" height="%d">' % (self.width, self.height)
		for i in self.items:
			head += i.asXML()

		head += '</svg>'

		return head

	def addElement(self, e):
		self.items.append(e)

	def save(self, filename):
		fd = open(filename, 'w')

		xml = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
		xml += self.asXML()

		fd.write(xml)
		fd.close()


