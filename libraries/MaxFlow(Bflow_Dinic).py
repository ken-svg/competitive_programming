from collections import deque
class MaxFlow(): # Dinic
  def __init__(self, N, B = None):
    self.N = N
    self.B = [0] * N
    if B is not None:
      for i in range(max(N, len(B))):
        self.B[i] = B[i]
    
    self.potential = [0] * N
    
    self.I = [[] for _ in range(N)]
    self.edges = []
    self.balance = [b for b in self.B]
    
    self.cost_scaling = False
  
  def is_balanced(self, S = -1, T = -1):
    return all([i == S or i == T or self.balance[i] == 0 for i in range(self.N)])
  
  def add_vertex(self, b = 0):
    self.N += 1
    self.B.append(b)
    self.balance.append(0)
    self.potential.append(0)
    self.I.append([])
    self.balance[self.N - 1] += b
  
  def set_vertex(self, v, b_new = 0):
    b_prv = self.B[v]
    if b_new == b_prv: return
    self.B[v] = b_new
    self.balance[v] += b_new - b_prv
    
  def add_edge(self, fr, to, cap, low = 0):
    flux = min(cap, max(low, 0))
    
    edge = [flux, to, cap, None]
    rev = [-flux, fr, -low, edge]
    edge[-1] = rev
    
    self.edges.append(edge)
    self.edges.append(rev)
    self.I[fr].append(edge)
    self.I[to].append(rev)
    
    if flux != 0:
      self.balance[fr] -= flux
      self.balance[to] += flux
    
  def set_edge(self, edge_id, cap_new, low_new = 0):
    edge = self.edges[edge_id << 1]
    rev = edge[-1]
    
    flux_new = min(max(edge[0], low_new), cap_new)
    flux_diff = flux_new - edge[0]
    
    self.balance[rev[1]] -= flux_diff # fr
    self.balance[edge[1]] += flux_diff # to
    edge[0] = flux_new
    rev[0] = -flux_new
    edge[2] = cap_new
    rev[2] = -low_new
    
  def _update_potential(self, delta = 1): # delta 緩和
    inf = 1 << 60
    #self._min_dist = inf = 1 << 60
    dist = [inf] * self.N
    balance = self.balance
    self.b_pos = [v for v in range(self.N) if balance[v] >= delta]
    if not self.b_pos: return
    task = deque(self.b_pos)
    vis = [False] * self.N
    for v in task:
      dist[v] = 0
      vis[v] = True
    
    #J = [[] for _ in range(self.N)]
    while task:
      p = task.popleft()
      d = dist[p]
      #if balance[p] <= -delta:
      #  self._min_dist = d
      #  break
        
      for edge in self.I[p]:
        flux, q, cap, rev = edge
        if vis[q] or cap - flux < delta: continue
        dist[q] = d + 1
        vis[q] = True
        task.append(q)
        #J[p].append(edge)
    
    #self.J = J
    self.potential = dist  
    
  
  def _find_path_and_flow(self, delta = 1): # delta 緩和
      edge_now = [0] * self.N
      I = self.I
      potential = self.potential
      balance = self.balance
      total = 0
      path = [None] * self.N
      min_cap = [0] * self.N
      for p in self.b_pos:
        if balance[p] < delta: continue
        now = p
        #print("set", p, self.potential)
        path_len = 0
        #ct = 0
        while path_len >= 0:
          #print(now, rest_now[now], flux_now[now], self.balance[now], edge_now[now], potential[I[now][edge_now[now]][1]] - potential[now] if edge_now[now] < len(I[now]) else None, I[now][edge_now[now]][0:3] if edge_now[now] < len(I[now]) else None)
          now = path[path_len - 1][-1][1] if path_len > 0 else p
          #print(now, path_len, total, min_cap)
          #ct += 1
          #if ct > 100: break
          
          if balance[now] <= -delta:
            flux_now = min(min_cap[path_len - 1], -balance[now])
            
            balance[now] += flux_now
            for l in range(path_len - 1, -1, -1):
              min_cap[l] -= flux_now
              rev = path[l]
              edge = rev[-1]
              edge[0] += flux_now
              rev[0] -= flux_now
              if edge[2] == edge[0]:
                edge_now[rev[1]] += 1
                path_len = l
              
            balance[p] -= flux_now
            total += flux_now
            if balance[p] == 0: break
            continue
          
          if edge_now[now] == len(I[now]):
            path_len -= 1
            if path_len == -1: break
            now = path[path_len][1]
            edge_now[now] += 1
            continue
          
          edge = I[now][edge_now[now]]
          to = edge[1]
          cap_rest = edge[2] - edge[0]
          if cap_rest == 0 or potential[to] - potential[now] != 1: #or (potential[to] >= self._min_dist and balance[to] >= 0):
            edge_now[now] += 1
            continue
          #print(now, edge, path, path_len)
          path[path_len] = edge[-1] # 逆辺
          min_cap[path_len] = min(min_cap[path_len - 1] if path_len > 0 else balance[p], cap_rest)
          path_len += 1
        
      return (total != 0)
  
  def find_flow(self):
    if all([self.balance[v] == 0 for v in range(self.N)]):
      return True
      
    delta = 1
    if self.cost_scaling:
      max_cap = 0
      for e in self.edges:
        if e[2] - e[0] > 0:
          max_cap = max(max_cap, e[2] - e[0])
      
      delta = 1 << max_cap.bit_length()
      
    # b-flowを解く
    while delta >= 1:
      flag = True
      while flag:
        self._update_potential(delta)
        if not self.b_pos: break
        #print("pot", self.potential)
        flag &= self._find_path_and_flow(delta)
      delta >>= 1
      
    return len(self.b_pos) == 0
  
  
  def maximize_flow_ST(self, S, T, max_flux = 1 << 60): # 解ありとなる最小のS->T流量
    # B[S] = B[T] = 0 が必要
    inf = 1 << 30
    
    if any([self.balance[v] != 0 for v in range(self.N)]):
      self.add_edge(T, S, cap = inf, low = 0) # T -> Sの辺で循環できるように
      self.find_flow()
      fail_flag = len(self.b_pos) > 0
      self.set_edge(-1, cap_new = 0)
      self.edges.pop()
      self.edges.pop()
      self.I[S].pop()
      self.I[T].pop()
    
      if fail_flag:
        return None # 充足不可能
    
    # S, Tに大きな流圧をかける
    self.set_vertex(S, max_flux)
    self.set_vertex(T, -max_flux)
    self.find_flow()
    #print(mcf)
    
    self.set_vertex(S, 0)
    self.set_vertex(T, 0)
    
    return self.balance[T]
    
  def __getitem__(self, e_id):
    edge = self.edges[e_id << 1]
    rev = edge[-1]
    return [edge[0], rev[1], edge[1], edge[2], -rev[2]]
    
  def __iter__(self):
    self._it = -1
    return self
    
  def __next__(self):
    if self._it + 1 >= len(self.edges) // 2: raise StopIteration
    self._it += 1
    return self[self._it]
    
  def __str__(self):
    ret = "MinCostFlow\n"
    ret += " Balance(now / set):\n   {:}\n".format(["{:}/{:}".format(v, w) for v, w in zip(self.balance, self.B)])
    ret += " Edges(fr -> to : flux (cap = [low, upp])):\n"
    for e in self:
      ret += "  {:} -> {:} : {:} (cap = [{:}, {:}])".format(e[1], e[2], e[0], e[4], e[3]) + "\n"
    ret.rstrip("\n")
    return ret
