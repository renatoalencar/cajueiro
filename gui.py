
import svg
import gtk
import random
import yaml

from avltree import *

def randomRange(i, j, k):
	n = []

	if abs(j - k) < i:
		raise IndexError('range is least than the size requested')

	while len(n) != i:
		r = random.randint(j, k)
		if not r in n:
			n.append(r)

	return n
		

class MainWindow(gtk.Window):
	def __init__(self, tree):
		gtk.Window.__init__(self)
		self.set_title('Cajueiro')

		vbox = gtk.VBox()
		
		if tree:
			self.tree = tree
		else:
			self.tree = AVLTree()

		self.image = gtk.Image()
		vbox.add(self.image)

		self.input = gtk.EntryBuffer('',0)
		entry = gtk.Entry()
		entry.set_buffer(self.input)
		vbox.add(entry)

		hbox = gtk.HBox()

		btn = gtk.Button(label="Insert")
		btn.connect("clicked", self.insert)
		hbox.add(btn)

		btn = gtk.Button(label="Insert from file")
		btn.connect('clicked', self.from_file)
		hbox.add(btn)

		btn = gtk.Button(label='Random')
		btn.connect('clicked', self.random)
		hbox.add(btn)

		btn = gtk.Button(label='Clear')
		btn.connect('clicked', self.clear)
		hbox.add(btn)

		vbox.add(hbox)

		hbox = gtk.HBox()

		btn = gtk.Button(label='Rotate RR')
		btn.connect('clicked', self.rotateRR)
		hbox.add(btn)

		btn = gtk.Button(label='Rotate LL')
		btn.connect('clicked', self.rotateLL)
		hbox.add(btn)

		btn = gtk.Button(label='Rotate RL')
		btn.connect('clicked', self.rotateRL)
		hbox.add(btn)

		btn = gtk.Button(label='Rotate LR')
		btn.connect('clicked', self.rotateLR)
		hbox.add(btn)

		vbox.add(hbox)

		hbox = gtk.HBox()

		btn = gtk.Button(label='Remove')
		btn.connect('clicked', self.remove)
		hbox.add(btn)

		btn = gtk.Button(label='Print')
		btn.connect('clicked', self.indented)
		hbox.add(btn)

		btn = gtk.Button(label='Save as PNG')
		btn.connect('clicked', self.save)
		hbox.add(btn)

		btn = gtk.Button(label='Shuffle')
		btn.connect('clicked', self.shuffle)
		hbox.add(btn)
		
		vbox.add(hbox)

		hbox = gtk.HBox()

		btn = gtk.Button(label='Save as YAML')
		btn.connect('clicked', self.saveYAML)
		hbox.add(btn)

		btn = gtk.Button(label='Load from YAML')
		btn.connect('clicked', self.loadYAML)
		hbox.add(btn)

		vbox.add(hbox)

		self.connect("destroy", gtk.main_quit)

		self.add(vbox)
		self.show_all()

	def loadYAML(self, obj):
		dialog = gtk.FileChooserDialog(
			'Choose the file to load',
			self,
			gtk.FILE_CHOOSER_ACTION_OPEN)
		dialog.add_button('Open', 1)
		dialog.add_button('Close', 2)

		if dialog.run() == 1:
			filename = dialog.get_filename()
			tree = yaml.load(open(filename))
			self.tree.loadFromTuple(tree)

		dialog.destroy()

		self.updateImage()

	def saveYAML(self, obj):
		dialog = gtk.FileChooserDialog(
			'Choose a place to save',
			self,
			gtk.FILE_CHOOSER_ACTION_SAVE)
		dialog.add_button('Save', 1)
		dialog.add_button('Close', 2)

		if dialog.run() == 1:
			filename = dialog.get_filename()
			open(filename, 'w').write(yaml.dump(self.tree.asTuple()))
		dialog.destroy()

	def shuffle(self, obj):
		nums = map(int, self.input.get_text().split())
		random.shuffle(nums)
		s = ''.join(map(lambda x: str(x)+' ', nums))
		self.input.set_text(s, len(s))

	def save(self, obj):
		dialog = gtk.FileChooserDialog(
			'Choose a place to save the tree',
			self,
			gtk.FILE_CHOOSER_ACTION_SAVE)
		dialog.add_button('Save', 1)
		dialog.add_button('Close', 2)

		if dialog.run() == 1:
			filename = dialog.get_filename()
			self.image.get_pixbuf().save(filename, 'png')
		dialog.destroy()

	def indented(self, obj):
		if self.tree.root:
			self.tree.root.show()

	def remove(self, obj):
		keys = map(int, self.input.get_text().split())

		for key in keys:
			node = self.tree.search(key)
			if node:
				node.remove()

		self.updateImage()

	def rotateRR(self, obj):
		key = int(self.input.get_text())
		node = self.tree.search(key)
		if node:
			r = node.rotateRR()
			if isinstance(r.parent, AVLTree):
				self.tree.root = r
			else:
				if r.value > r.parent.value:
					r.parent.right = r
				else:
					r.parent.left = r

		self.updateImage()

	def rotateLL(self, obj):
		key = int(self.input.get_text())
		node = self.tree.search(key)
		if node:
			r = node.rotateLL()
			if isinstance(r.parent, AVLTree):
				self.tree.root = r
			else:
				if r.value > r.parent.value:
					r.parent.right = r
				else:
					r.parent.left = r

		self.updateImage()

	def rotateRL(self, obj):
		key = int(self.input.get_text())
		node = self.tree.search(key)
		if node:
			r = node.rotateRL()
			if isinstance(r.parent, AVLTree):
				self.tree.root = r
			else:
				if r.value > r.parent.value:
					r.parent.right = r
				else:
					r.parent.left = r

		self.updateImage()

	def rotateLR(self, obj):
		key = int(self.input.get_text())
		node = self.tree.search(key)
		if node:
			r = node.rotateLR()
			if isinstance(r.parent, AVLTree):
				self.tree.root = r
			else:
				if r.value > r.parent.value:
					r.parent.right = r
				else:
					r.parent.left = r

		self.updateImage()



	def clear(self, obj):
		self.tree.root = None
		self.image.clear()
		self.input.set_text('', 0)
		#self.resize(-1,-1)

	def insert(self, obj):
		nums = map(int, self.input.get_text().split())

		for i in nums:
			self.tree.insert(i)
		self.updateImage()

	def updateImage(self):
		if self.tree:
			save_tree_as_svg(self.tree)
		self.image.set_from_file('tree.svg')

	def from_file(self, obj):
		nums = map(int, open('input.txt').read().split('.')[0].split(';'))

		for i in nums:
			self.tree.insert(i)

		self.updateImage()

	def random(self, obj):
		n = map(int, self.input.get_text().split())
		
		if len(n) == 1:
			nums = randomRange(n[0], 0, 50)
		elif len(n) == 2:
			nums = randomRange(n[0], 0, n[1])
		elif len(n) == 3:
			nums = randomRange(n[0], n[1], n[2])

		s = ''.join(map(lambda x: str(x)+' ', nums))

		self.input.set_text(s, len(s))

def save_tree_as_svg(tree):

	if tree.root:
		tree.root.updateLevels()
	items = tree.inOrder()

	img = svg.SVG((len(items) + 3)* 32, (tree.height() + 2) * 32)

	for i in range(tree.height() + 1):
		img.addElement(svg.Text((len(items) + 2) * 32, (i + 1) * 32,
			str(i), 14))

	nodes = []
	for i in range(len(items)):
		c = svg.Circle((i + 1) * 32,
			(items[i].level + 1) * 32, 15)

		if items[i].left:
			p = items.index(items[i].left)
			node = items[p]
			img.addElement(svg.Line(c.cx, c.cy,
				(p + 1) * 32,
				(node.level + 1) * 32))
		if items[i].right:
			p = items.index(items[i].right)
			node = items[p]
			img.addElement(svg.Line(c.cx, c.cy,
				(p + 1) * 32,
				(node.level + 1) * 32))

		#img.addElement(c)
		nodes.append((c, svg.Text(c.cx, c.cy, str(items[i].value), 14,
			'' if items[i].balance() in [-1,0,1] else 'fill:#ff0000')))
		img.addElement(svg.Text(c.cx - 14, c.cy - 14, str(items[i].balance()), 10, "fill:#ff0000;border:1pt solid #ffffff"))

	for i in nodes:
		img.addElement(i[0])
		img.addElement(i[1])
	img.save('tree.svg')
