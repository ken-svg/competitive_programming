class LinkedList():
  def __init__(self, A = []):
    self.head = A[0] if A else None
    self.tail = A[-1] if A else None
    
    self.len = len(A)
    
    self.left = {}
    self.right = {}
    for i in range(len(A) - 1):
      a = A[i]
      b = A[i + 1]
      self.right[a] = b
      self.left[b] = a
      
    self.left[self.head] = None
    self.right[self.tail] = None
    
  def append(self, v, l = None): # insert v on the right of l
    if self.len == 0:
      self.left[v] = None
      self.right[v] = None
      self.head = v
      self.tail = v
      self.len = 1
      return 
      
    if l is None: l = self.tail
    r = self.right[l]
    self.right[l] = v
    self.right[v] = r
    self.left[v] = l
    if r is not None:
      self.left[r] = v
    else: # l == self.tail
      self.tail = v
      
    self.len += 1
      
  def appendleft(self, v, r = None): # insert v on the left of r
    if self.len == 0:
      self.left[v] = None
      self.right[v] = None
      self.head = v
      self.tail = v
      self.len = 1
      return 
    
    if r is None: r = self.head
    l = self.left[r]
    self.left[r] = v
    self.left[v] = l
    self.right[v] = r
    if l is not None:
      self.right[l] = v
    else: # r == self.head
      self.head = v
      
    self.len += 1
      
  def pop(self, v = None): # pop v
    l = self.left[v]
    r = self.right[v]
    if self.head == v:
      self.head = r
    if self.tail == v:
      self.tail = l
    
    if l is not None:
      self.right[l] = r
    if r is not None:
      self.left[r] = l
    self.left[v] = None
    self.right[v] = None
      
    self.len -= 1  
      
  def __list__(self):
    A = []
    now = self.now
    while now is not None:
      A.append(now)
      now = self.right[now]
      
  def __str__(self):
    return str(list(self))
  
  def __iter__(self):
    now = self.head
    while now is not None:
      yield now
      now = self.right[now]
      
  def __len__(self):
    return self.len
