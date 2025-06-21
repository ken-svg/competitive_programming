from collections import deque
from heapq import heappop, heappush
class MinCostFlow(): # primal dual
  def __init__(self, N, B = None, pot = None):
    self.N = N
    self.B = [0] * N
    if B is not None:
      for i in range(max(N, len(B))):
        self.B[i] = B[i]
    
    self.potential = [0] * N
    if pot is not None:
      for i in range(max(N, len(pot))):
        self.potential[i] = pot[i]
    
    self.I = [[] for _ in range(N)]
    self.edges = []
    self.balance = [b for b in self.B]
    
    self.b_pos = set([i for i in range(N) if self.balance[i] > 0])
    self.b_neg = set([i for i in range(N) if self.balance[i] < 0])
    
    self.total_cost = 0
  
  def is_balanced(self):
    return not(self.b_pos)
    
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
  
  def add_vertex(self, b = 0, p = 0):
    self.N += 1
    self.B.append(b)
    self.balance.append(0)
    self.potential.append(p)
    self.I.append([])
    self._update_balance(self.N - 1, b)
  
  def set_vertex(self, v, b_new = 0):
    b_prv = self.B[v]
    if b_new == b_prv: return
    self.B[v] = b_new
    self._update_balance(v, b_new - b_prv)
    
  def add_edge(self, fr, to, cost, cap, low = 0):
    flux = low if cost + self.potential[fr] - self.potential[to] >= 0 else cap
    self.total_cost += flux * cost
    
    edge = [flux, to, cost, cap, None]
    rev = [-flux, fr, -cost, -low, edge]
    edge[-1] = rev
    self.edges.append(edge)
    self.edges.append(rev)
    self.I[fr].append(edge)
    self.I[to].append(rev)
    self._update_balance(fr, -flux)
    self._update_balance(to, flux)
    
  def set_edge(self, edge_id, cost_new, cap_new, low_new = 0):
    edge = self.edges[edge_id << 1]
    rev = edge[-1]
    self.total_cost -= edge[0] * edge[2]
    
    red_cost_new = cost_new + self.potential[rev[1]] - self.potential[edge[1]]
    if red_cost_new == 0:
      flux_new = min(max(edge[0], low_new), cap_new)
    else:
      flux_new = low_new if red_cost_new >= 0 else cap_new
    edge = self.edges[edge_id << 1]
    
    flux_diff = flux_new - edge[0]
    self._update_balance(rev[1], -flux_diff) # fr
    self._update_balance(edge[1], flux_diff) # to
    edge[0] = flux_new
    rev[0] = -flux_new
    edge[2] = cost_new
    rev[2] = -cost_new
    edge[3] = cap_new
    rev[3] = -low_new
    self.total_cost += edge[0] * edge[2]
    
  def _update_potential(self):
    dist = [-1] * self.N
    task = [[0, v] for v in self.b_pos]
    vis = [False] * self.N
    while task:
      d, p = heappop(task)
      if vis[p]: continue
      vis[p] = True
      dist[p] = d
      
      for edge in self.I[p]:
        flux, q, cost, cap, rev = edge
        if vis[q] or cap == flux: continue
        heappush(task, [d + cost + self.potential[p] - self.potential[q], q])
        
    max_dist = max(dist)
    for i in range(self.N):
      if dist[i] != -1:
        self.potential[i] += dist[i]
      else:
        self.potential[i] += max_dist
      
  def find_flow(self):
    flag = True
    while flag:
      self._update_potential()
      task = deque([v for v in self.b_pos])
      prv = [None] * self.N
      vis = [self.balance[v] > 0 for v in range(self.N)]
      while task:
        p = task.popleft()
        for edge in self.I[p]:
          flux, q, cost, cap, rev = edge
          if vis[q] or cost + self.potential[p] - self.potential[q] != 0 or cap == flux: continue
          task.append(q)
          prv[q] = rev
          vis[q] = True
          
      flag = False
      for v in list(self.b_neg):
        flux_now = -self.balance[v]
        v_now = v
        path = []
        while prv[v_now] is not None and self.balance[v_now] <= 0:
          rev = prv[v_now]
          flux_now = min(flux_now, rev[-1][3] - rev[-1][0])
          v_now = rev[1]
          path.append(rev)
        
        flux_now = min(flux_now, max(0, self.balance[v_now]))
        self._update_balance(v_now, -flux_now)
        self._update_balance(v, flux_now)
        flag |= (flux_now > 0)
        for rev in path:
          rev[0] -= flux_now
          rev[-1][0] += flux_now
          self.total_cost += -flux_now * rev[2]
    return len(self.b_pos) == 0
      
  def minimize_flow_ST(self, S, T): # 解ありとなる最小のS->T流量
    # B[S] = B[T] = 0 が必要
    inf = 1 << 30
    
    self.add_edge(T, S, cost = inf, cap = inf, low = 0) # T -> Sの辺で循環できるように
    self.find_flow()
    fail_flag = len(self.b_pos) > 0
    self.set_edge(-1, cost_new = 0, cap_new = 0)
    self.edges.pop()
    self.edges.pop()
    self.I[S].pop()
    self.I[T].pop()
    
    if fail_flag:
      return -1 # 充足不可能
    else:
      return self.balance[S]
  
  def minimize_cost_ST(self, S, T): # 解の中でコストを最小化（S->T流量は自由）
    # B[S] = B[T] = 0 が必要
    
    # step1: 解ありとなる最小流量(S -> T)を求める 
    v = self.minimize_flow_ST(S, T)
    if v == -1:
      return None # 充足不可能
    
    # step2: S -> T流量を自由化したうえで最小コストを求める
    inf = 1 << 30
    
    self.set_vertex(S, inf)
    self.set_vertex(T, -inf)
    self.add_edge(S, T, cost = 0, cap = inf, low = 0)
    self.find_flow()
    
    mp = min(self.potential)
    self.potential = [v - mp for v in self.potential]
    
    self.set_edge(-1, cost_new = 0, cap_new = 0)
    self.edges.pop()
    self.edges.pop()
    self.I[S].pop()
    self.I[T].pop()
    
    self.set_vertex(S, 0)
    self.set_vertex(T, 0)
    
    return self.total_cost
    
    
  def __getitem__(self, e_id):
    edge = self.edges[e_id << 1]
    rev = edge[-1]
    return [edge[0], rev[1], edge[1], edge[2], edge[3], -rev[3]]
    
  def __iter__(self):
    self._it = -1
    return self
    
  def __next__(self):
    if self._it + 1 >= len(self.edges) // 2: raise StopIteration
    self._it += 1
    return self[self._it]
    
  def __str__(self):
    ret = "MinCostFlow\n"
    ret += " total_cost: {:} \n".format(self.total_cost)
    ret += " Potential:\n   {:}\n".format(self.potential)
    ret += " Balance(now / set):\n   {:}\n".format(["{:}/{:}".format(v, w) for v, w in zip(self.balance, self.B)])
    ret += " Edges(fr -> to : flux (cost, cap = [low, upp])):\n"
    for e in self:
      ret += "  {:} -> {:} : {:} (cost = {:}, cap = [{:}, {:}])".format(e[1], e[2], e[0], e[3], e[5], e[4]) + "}\n"
    ret.rstrip("\n")
    return ret
    

N, M = map(int,input().split())
if N == 0:
  print(0)
  exit()
B = [int(input()) for _ in range(N)]
mcf = MinCostFlow(N, B)

for _ in range(M):
  s, t, l, u, c = map(int,input().split())
  mcf.add_edge(s, t, c, u, l)
  
mcf.find_flow()
#print(mcf.b_neg)

if not mcf.is_balanced():
  print("infeasible")
else:
  print(mcf.total_cost)
  for v in mcf.potential:
    print(v)
  for e in mcf.edges[::2]:
    print(e[0])
