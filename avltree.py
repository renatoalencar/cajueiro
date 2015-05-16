

class Node:
	def __init__(self, value, parent=None):
		self.value = value
		self.parent = parent
		self.left = None
		self.right = None

		self.level = 0
	
	def height(self):
		return (0 if self.isLeaf() else self.maxChildrenHeight() + 1)

	def updateLevels(self):
		if not isinstance(self.parent, AVLTree):
			self.level = self.parent.level + 1
		else:
			self.level = 0

		if self.left:
			self.left.updateLevels()
		if self.right:
			self.right.updateLevels()

	def isLeaf(self):
		return (not self.left and not self.right)

	def maxChildrenHeight(self):
		if self.left and self.right:
			return max(self.left.height(), self.right.height())
		elif self.right:
			return self.right.height()
		elif self.left:
			return self.left.height()
		else:
			return -1

	def balance(self):
		return (self.left.height() if self.left else -1) - (self.right.height() if self.right else -1)

	def insert(self, node):
		node.parent = self

		if node.value < self.value:
			if self.left:
				self.left.insert(node)
			else:
				self.left = node
		if node.value > self.value:
			if self.right:
				self.right.insert(node)
			else:
				self.right = node

		while not isinstance(node, AVLTree):
			if node.balance() in [-2, 2]:
				parent = node.parent
				root = node.rebalance()
	
				if parent:
					if isinstance(parent, AVLTree):
						parent.root = root
					elif root.value > parent.value:
						parent.right = root
					elif root.value < parent.value:
						parent.left = root

			node = node.parent

	def remove(self):
		if self.right and self.left:
			if self.right.height() < self.left.height():
				node = self.right
				while node.left:
					node = node.left
			else:
				node = self.left
				while node.right:
					node = node.right
			
			node.remove()
			node.parent = self.parent
			node.left = self.left
			node.right = self.right

			if self.left:
				self.left.parent = node
			if self.right:
				self.right.parent = node

			if isinstance(node.parent, AVLTree):
				node.parent.root = node
			else:
				if node.value > node.parent.value:
					node.parent.right = node
				elif node.value < node.parent.value:
					node.parent.left = node			
				
		elif self.right:
			node = self.right
			if isinstance(self.parent, AVLTree):
				self.parent.root = node
			elif self.value > self.parent.value:
				self.parent.right = node
			elif self.value < self.parent.value:
				self.parent.left = node
			node.parent = self.parent
		elif self.left:
			node = self.left
			if isinstance(self.parent, AVLTree):
				self.parent.root = node
			elif self.value > self.parent.value:
				self.parent.right = node
			elif self.value < self.parent.value:
				self.parent.left = node
			node.parent = self.parent

		else:
			if isinstance(self.parent, AVLTree):
				self.parent.root = None
				return

			if self.value > self.parent.value:
				self.parent.right = None
			elif self.value < self.parent.value:
				self.parent.left = None

		#return
		node = self.parent
		while not isinstance(node, AVLTree):
			if node.balance() not in [-1,0,1]:
				n = node.rebalance()
				if isinstance(n.parent, AVLTree):
					n.parent.root = n
				else:
					if n.value > n.parent.value:
						n.parent.right = n
					if n.value < n.parent.value:
						n.parent.left = n
			node = node.parent
	
			
	def rebalance(self):
		if self.balance() == -2:
			if self.right.balance() in [-1, 0]:
				n = self.rotateRR()
				assert n is not None
				return n
			elif self.right.balance() == 1:
				n = self.rotateRL()
				assert n is not None
				return n
		if self.balance() == 2:
			if self.left.balance() in [1, 0]:
				n = self.rotateLL()
				assert n is not None
				return n
			elif self.left.balance() == -1:
				n = self.rotateLR()
				assert n is not None
				return n

		return self

	def preOrder(self):
		r = [self]
		if self.left:
			r += self.left.preOrder()
		if self.right:
			r += self.right.preOrder()

		return r

	def inOrder(self):
		r = []
		if self.left:
			r += self.left.inOrder()
		r += [self]
		if self.right:
			r += self.right.inOrder()

		return r

	def postOrder(self):
		r = []
		if self.left:
			r += self.left.postOrder()
		if self.right:
			r += self.right.postOrder()
		r += [self]

	def rotateRR(self):
		parent = self.parent

		B = self.right
		self.right = B.left
		
		if self.right:
			self.right.parent = self

		B.left = self
		self.parent = B
		B.parent = parent

		return B

	def rotateLL(self):
		parent = self.parent

		B = self.left
		self.left = B.right

		if self.left:
			self.left.parent = self

		B.right = self
		self.parent = B
		B.parent = parent

		return B

	def rotateLR(self):
		self.left = self.left.rotateRR()
		#self.left.parent = self
		return self.rotateLL()

	def rotateRL(self):
		self.right = self.right.rotateLL()
		#self.right.parent = self
		return self.rotateRR()

	def search(self, key):
		if self.value == key:
			return self

		if key > self.value and self.right:
			return self.right.search(key)
		if key < self.value and self.left:
			return self.left.search(key)

	def show(self, n=0):
		print n*'\t' + "%d (%s FB: %d)" % (self.value,
			'raiz' if n == 0 else ('pai: %d' % self.parent.value),
			self.balance())
		
		if self.left:
			self.left.show(n + 1)
		if self.right:
			self.right.show(n + 1)

	def asTuple(self):
		return (self.value,
			self.left.asTuple() if self.left else None,
			self.right.asTuple() if self.right else None)

	def loadTuple(self, t):
		self.value = t[0]
		if t[1]:
			self.left = Node(0, self)
			self.left.loadTuple(t[1])
		if t[2]:
			self.right = Node(0, self)
			self.right.loadTuple(t[2])


class AVLTree:
	def __init__(self, *args):
		self.root = None

		if len(args) == 1 and isinstance(args[0], list):
			for i in args[0]:
				self.insert(i)
		else:
			for i in args:
				self.insert(i)

	def height(self):
		if self.root:
			return self.root.height()
		
		return 0

	def insert(self, value):
		if self.root:
			self.root.insert(Node(value))
		else:
			n = Node(value)
			n.parent = self
			self.root = n

		self.root.updateLevels()

	def preOrder(self):
		return (self.root.preOrder() if self.root else [])

	def inOrder(self):
		return (self.root.inOrder() if self.root else [])

	def postOrder(self):
		return (self.root.postOrder() if self.root else [])

	def search(self, key):
		return (self.root.search(key) if self.root else None)

	def asTuple(self):
		return self.root.asTuple() if self.root else ()

	def loadFromTuple(self, t):
		self.root = Node(0, self)
		self.root.loadTuple(t)
		self.root.updateLevels()
