class perpetuated_array():
  def __init__(self, A, N = None):
    if N is None: self.N = N = len(A)
    A = A + [0] * (N - len(A))
    task = [[A[i]] for i in range(len(A))]
    while len(task) > 1:
      task_next = []
      for j in range(0, len(task), 2):
        v = [None, task[j], task[j+1] if len(task) > j+1 else None]
        task_next.append(v)
      task = task_next
    self.initial = [task[0]]
    self.version_num = 1
    
  def update(self, version, i, x): # A_version[i] <- x
    initial = self.initial
    N = self.N
    self.version_num += 1
    now = initial[version]
    now_copy = [None]
    initial.append(now_copy)
    for b in range((N-1).bit_length()-1, -1, -1):
      c = (i >> b) & 1
      copy_next = [None]
      if c:
        now_copy.append(now[1])
        now_copy.append(copy_next)
        now = now[2]
      else:
        now_copy.append(copy_next)
        now_copy.append(now[2])
        now = now[1]
      now_copy = copy_next
    now_copy[0] = x
    #nowx_copy += [None] * 2
    return self.version_num
    
  def value_at(self, version, i):
    N = self.N
    now = self.initial[version]
    for b in range((N-1).bit_length()-1, -1, -1):
      if (i >> b) & 1:
        now = now[2]
      else:
        now = now[1]
    return now[0]
