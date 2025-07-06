import pypyjit
pypyjit.set_param('max_unroll_recursion=-1')
import sys
sys.setrecursionlimit(3 * 10 ** 5)

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
    
    self.b_pos = set([i for i in range(N) if self.balance[i] > 0])
    self.b_neg = set([i for i in range(N) if self.balance[i] < 0])
    
    self.cost_scaling = False
  
  def is_balanced(self, S = -1, T = -1):
    return all([i == S or i == T or self.balance[i] == 0 for i in range(self.N)])
    
  def _update_balance(self, v, db):
    if db == 0: return
    b = self.balance[v]
    flag = (b * db <= 0 and abs(b) <= abs(db))
    if flag:
      if b > 0: self.b_pos.remove(v)
      elif b < 0: self.b_neg.remove(v)
    self.balance[v] += db
    if flag:
      b = self.balance[v]
      if b > 0: self.b_pos.add(v)
      elif b < 0: self.b_neg.add(v)
  
  def add_vertex(self, b = 0):
    self.N += 1
    self.B.append(b)
    self.balance.append(0)
    self.potential.append(0)
    self.I.append([])
    self._update_balance(self.N - 1, b)
  
  def set_vertex(self, v, b_new = 0):
    b_prv = self.B[v]
    if b_new == b_prv: return
    self.B[v] = b_new
    self._update_balance(v, b_new - b_prv)
    
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
      self._update_balance(fr, -flux)
      self._update_balance(to, flux)
    
  def set_edge(self, edge_id, cap_new, low_new = 0):
    edge = self.edges[edge_id << 1]
    rev = edge[-1]
    
    flux_new = min(max(edge[0], low_new), cap_new)
    flux_diff = flux_new - edge[0]
    
    self._update_balance(rev[1], -flux_diff) # fr
    self._update_balance(edge[1], flux_diff) # to
    edge[0] = flux_new
    rev[0] = -flux_new
    edge[2] = cap_new
    rev[2] = -low_new
    
  def _update_potential(self, delta = 1): # delta 緩和
    inf = 1 << 60
    dist = [inf] * self.N
    task = deque([v for v in self.b_pos if self.balance[v] >= delta])
    vis = [False] * self.N
    for v in task:
      dist[v] = 0
      vis[v] = True
    
    while task:
      p = task.popleft()
      d = dist[p]
      
      for edge in self.I[p]:
        flux, q, cap, rev = edge
        #print(q, cap, flux)
        if vis[q] or cap - flux < delta: continue
        dist[q] = d + 1
        vis[q] = True
        task.append(q)
    
    self.potential = dist    
  
  def _find_dfs(self, p, flux_upper, edge_num, I, potential, delta = 1): # delta 緩和
    _find_dfs = self._find_dfs
    rest = flux_upper
    if self.balance[p] < 0:
      flux_diff = min(rest, -self.balance[p])
      self._update_balance(p, flux_diff) # self.balance[p] += flux_diff
      rest -= flux_diff
    
    I_p = I[p]
    e_p = edge_num[p]
    pot_p = potential[p]
    while rest and e_p < len(I_p):
      edge = I_p[e_p]
      flux, q, cap, rev = edge
      if potential[q] - pot_p != 1 or cap - flux < delta:
        flux_diff = 0
      else:
        flux_diff = _find_dfs(q, min(rest, cap - flux), edge_num, I, potential, delta)
      
      if flux_diff == 0:
        edge_num[p] += 1
      
      else:
        edge[0] += flux_diff
        rev[0] -= flux_diff
        rest -= flux_diff
        if rest and cap - edge[0] > 0:
          edge_num[p] += 1
          
      e_p = edge_num[p]
    
    return flux_upper - rest  
    
  def _find_path_and_flow(self, delta = 1): # delta 緩和
      edge_num = [0] * self.N
      total = 0
      b_po = list(self.b_pos)
      for p in b_po:
        flux_diff = self._find_dfs(p, self.balance[p], edge_num, self.I, self.potential, delta)
        self._update_balance(p, -flux_diff) # self.balance[p] -= flux_diff
        total += flux_diff
      return (total != 0)
  
  def find_flow(self):
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
        #print("pot", self.potential)
        flag &= self._find_path_and_flow(delta)
      delta >>= 1
      
    return len(self.b_pos) == 0
  
  
  def maximize_flow_ST(self, S, T, max_flux = 1 << 60): # 解ありとなる最小のS->T流量
    # B[S] = B[T] = 0 が必要
    inf = 1 << 30
    
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
    max_flux = 1 << 60
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
