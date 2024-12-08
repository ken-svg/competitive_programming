from collections import deque
class PersistentArray():
  def __init__(self, N, initial_data = []):
    # N >= 2とする
    self.N = N
    self.rank = (N-1).bit_length()
    self.L = 1 << self.rank
    self.time_now = 0
    
    self.entry = [[None, None]]
    
    entry_point = self.entry[0]
    task = deque([entry_point])
    for _ in range(self.L - 1):
      p = task.popleft()
      l = p[0] = [None, None]
      r = p[1] = [None, None]
      task.append(l)
      task.append(r)
    
    if len(initial_data) < self.L:
      initial_data.extend([None] * (self.L - len(initial_data)))
    
    p, edge_done, ind = entry_point, 0, 0
    #task = [[entry_point, 0, 0]]
    path = [[entry_point, 0, 0]]
    while path:
      if p[1] is None:
        p[0] = initial_data[ind]
        edge_done = 2
      
      if edge_done == 2:
        path.pop()
        if path:
          p, edge_done, ind = path[-1]
        continue
      
      p, edge_done, ind = p[edge_done], 0, ind | (edge_done << (len(path) - 1))
      path[-1][1] += 1
      path.append([p, edge_done, ind])
        
  def update(self, t, i, v): # 時刻tでのarray[i]をvで更新する。同時に最新時刻を割り当てる。
    self.time_now += 1
    #t_new = self.time_now
    
    p = self.entry[t]
    #p_new = [None, None]
    #self.entry.append(p_new)
    
    task = []
    for r in range(self.rank):
      task.append([p[(i % 2) ^ 1], i % 2])
      p = p[i % 2]
      i >>= 1
    
    q = [v, None]
    task.reverse()
    for p, s in task:
      if s:
        q = [p, q]
      else:
        q = [q, p]
    self.entry.append(q)  
      
    """  
      if i % 2:
        p_new[0] = p[0]
        p = p[1]
        p_new[1] = [None, None]
        p_new = p_new[1]
        p_new = [p[0], p_new[1]]
        p = p[1]
        
      else:
        p_new[1] = p[1]
        p = p[0] 
        p_new[0] = [None, None]
        p_new = p_new[0]
      
      if r == 0:
        self.entry.append(p_new)
        
      i >>= 1
    p_new[0] = v    
    """
    
  def value(self, t, i): # 時刻tでのarray[i]を返す
    p = self.entry[t]
    for r in range(self.rank):
      p = p[i % 2]
      i >>= 1
    return p[0]
  
  def array(self, t): #時刻tでのarrayを返す
    entry_point = self.entry[t]
    p, edge_done, ind = entry_point, 0, 0
    path = [[entry_point, 0, 0]]
    ans = [0] * self.L
    while path:
      if p[1] is None:
        ans[ind] = p[0]
        edge_done = 2
      
      if edge_done == 2:
        path.pop()
        if path:
          p, edge_done, ind = path[-1]
        continue
      
      p, edge_done, ind = p[edge_done], 0, ind | (edge_done << (len(path) - 1))
      path[-1][1] += 1
      path.append([p, edge_done, ind])
    
    return ans[:N] 
