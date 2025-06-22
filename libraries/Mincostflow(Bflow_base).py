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
    
    self.cost_scaling = False
    
  def activate_cost_scaling(self):
    self.cost_scaling = True
    
  def disable_cost_scaling(self):
    self.cost_scaling = False
  
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
    
  def _update_potential(self, delta = 1): # delta 緩和
    dist = [-1] * self.N
    task = [[0, v] for v in self.b_pos if self.balance[v] >= delta]
    vis = [False] * self.N
    while task:
      d, p = heappop(task)
      if vis[p]: continue
      vis[p] = True
      dist[p] = d
      
      for edge in self.I[p]:
        flux, q, cost, cap, rev = edge
        if vis[q] or cap - flux < delta: continue
        heappush(task, [d + cost + self.potential[p] - self.potential[q], q])
        
    max_dist = max(dist)
    for i in range(self.N):
      if dist[i] != -1:
        self.potential[i] += dist[i]
      else:
        self.potential[i] += max_dist
  
  def _find_path_and_flow(self, record_point = None, record_list = None, delta = 1):
      task = deque([v for v in self.b_pos if self.balance[v] >= delta])
      prv = [None] * self.N
      vis = [self.balance[v] >= delta for v in range(self.N)]
      while task:
        p = task.popleft()
        for edge in self.I[p]:
          flux, q, cost, cap, rev = edge
          if vis[q] or cost + self.potential[p] - self.potential[q] != 0 or cap == flux: continue
          task.append(q)
          #print(p, q)
          prv[q] = rev
          vis[q] = True
          
      flag = False
      for v in list(self.b_neg):
        if self.balance[v] > -delta: continue
        flux_now = -self.balance[v]
        v_now = v
        path = []
        while prv[v_now] is not None and self.balance[v_now] < delta:
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
          
        if flux_now > 0 and record_point is not None:
          record_list.append([self.balance[record_point], self.total_cost])
      return flag    
  
  def find_flow(self, record_point = None, record_list = None):
    if self.cost_scaling:
      self._find_flow_with_cost_scaling()
    
    else:    
      flag = True
      if record_point is not None:
        record_list.append([self.balance[record_point], self.total_cost])
      while flag:
        self._update_potential()
        flag &= self._find_path_and_flow(record_point, record_list)
      
    return len(self.b_pos) == 0
  
  def _find_flow_with_cost_scaling(self):
    max_cap = 0
    for e in self.edges:
      if e[3] - e[0] > 0:
        max_cap = max(max_cap, e[3] - e[0])
    
    delta = 1 << max_cap.bit_length()
    while delta > 1:
      delta >>= 1
      
      # 負辺除去
      for e in self.edges:
        to = e[1]
        fr = e[-1][1]
        if e[3] - e[0] >= delta and e[2] + self.potential[fr] - self.potential[to] < 0:
          v = e[3] - e[0]
          e[0] += v
          e[-1][0] -= v
          self._update_balance(fr, -v)
          self._update_balance(to, v)
          self.total_cost += e[2] * v
      
      flag = True
      while flag:
        self._update_potential(delta = delta)
        flag &= self._find_path_and_flow(delta = delta)
  
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
      
  def maximize_flow_ST(self, S, T): # 解ありとなる最大のS->T流量
    # B[S] = B[T] = 0 が必要
    inf = 1 << 30
    
    self.add_edge(T, S, cost = 0, cap = inf, low = 0) # T -> Sの辺で循環できるように
    self.find_flow()
    fail_flag = len(self.b_pos) > 0
    self.set_edge(-1, cost_new = 0, cap_new = 0)
    self.edges.pop()
    self.edges.pop()
    self.I[S].pop()
    self.I[T].pop()
    
    if fail_flag:
      return -1 # 充足不可能
    
    # S, Tに大きな流圧をかける
    inf = 1 << 30
    self.set_vertex(S, inf)
    self.set_vertex(T, -inf)
    self.find_flow()
    self.I[S].pop()
    self.I[T].pop()
    
    self.set_vertex(S, 0)
    self.set_vertex(T, 0)
    
    return self.balance[S]
  
  def flow_cost_slope_ST(self, S, T): # 流量とコストのスロープを作成（S->T流量は自由）
    # B[S] = B[T] = 0 が必要
    
    # step1: 解ありとなる最小流量(S -> T)を求める 
    v = self.minimize_flow_ST(S, T)
    if v == -1:
      return None # 充足不可能
    
    # step2: S -> T流量を自由化したうえで最小コストを求める
    inf = 1 << 30
    
    self.set_vertex(S, inf)
    self.set_vertex(T, -inf)
    
    record_list = []
    self.find_flow(S, record_list)
    
    self.set_vertex(S, 0)
    self.set_vertex(T, 0)
    
    return [[inf - b, v] for b, v in record_list]
    
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
      ret += "  {:} -> {:} : {:} (cost = {:}, cap = [{:}, {:}])".format(e[1], e[2], e[0], e[3], e[5], e[4]) + "\n"
    ret.rstrip("\n")
    return ret

# 入力関係    
#  self.__init__(N, B, pot) # 頂点数Nのグラフを作る。B：入力流量、pot：初期ポテンシャル（適切であれば高速化に寄与）
#  self.add_edge(fr, to, cost, cap, low = 0) # 辺追加： fr -> to (cost, [low, cap]) 
#  self.cost_scaling # Trueならcost scaling (O(ElogF*(Dijkstara)))。FalseならO(F*(Dijkstara))

# 状態取得
#  print(self) # 内部状態を出力
#  self.is_balanced() # 入力流量が解消していればTrue
#  self[e_id] # e_id番目の辺状態を出力 [flow, fr, to, cost, cap, low]　（for文でイテレーション可）
#  self.balance　# 各点の保持流量
#  self.potential # 各点のポテンシャル

# 求解
#  self.find_flow() # 流量制約を満たし、入力流量を解消する（feasibleな）解を発見（存在しないときはFalseを返す）
#  self.minimize_flow_ST(S, T) # S->T流量を自由とたfeasibleな解のなかで、最小のS->T流量を返す
#  self.maximize_flow_ST(S, T) # S->T流量を自由とたfeasibleな解のなかで、最大のS->T流量を返す
#  self.minimize_cost_ST(S, T) # S->T流量を自由とたfeasibleな解のなかで、最小コストを返す
#  self.flow_cost_slope_ST(S, T) 
#   # [self.cost_scaling = Falseを要求] S->T流量を自由とし、feasibleな解のなかで、[S->T流量, cost]の下凸曲線を返す（はず。未検証）
