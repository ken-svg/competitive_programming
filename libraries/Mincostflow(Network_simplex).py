import pypyjit
pypyjit.set_param('max_unroll_recursion=-1')
from collections import deque
from math import isqrt
class MinCostFlow_NS(): # network_simplex法
  def __init__(self, N, B = None):
    self.N = N
    self.B = [0] * N
    if B is not None:
      for i in range(max(N, len(B))):
        self.B[i] = B[i]
        
    self.I = [[] for _ in range(N)]
    self.edges = []
    self.balance = [b for b in self.B]
    self.prv = [None] * self.N # 親へ戻る辺を管理
    self.potential = [0] * self.N 
    self._in_neg = [self.balance[v] < 0 for v in range(self.N)]
    self._root = [i for i in range(self.N)]
    self._candidate_edges = deque([])
    
    self._tmp = 0
    
    # 以後森を管理。
    # 各木について「残存する湧き出し、吸い込みは親頂点にしかない」、「任意の点から親頂点へ供給可能」を保つ。
    # 初期状態は完全非連結（全ての点が親）
    self.total_cost = 0
    
  def is_balanced(self):
    return all([v == 0 for v in self.balance])
  
  def _pick_edge(self):
    if not self.edges:
      return None
    obj = self._tmp
    first_flag = True
    end_flag = False
    
    _bucket = isqrt(len(self.edges)) + 1
    while not end_flag:
      target = None
      cost_now = 0
      for edge in self.edges[self._tmp: self._tmp + _bucket]:
        if (not first_flag) and obj == self._tmp:
          end_flag = True
          
        self._tmp += 1
        self._tmp %= len(self.edges)
        first_flag = False
        
        if self.prv[edge[1]] is edge[-1] or self.prv[edge[-1][1]] is edge: continue # 木辺
        if edge[3] - edge[0] == 0: continue # 飽和
        fr = edge[-1][1]
        to = edge[1]
        if (self._in_neg[to]) and (not self._in_neg[fr]):
          return edge
        if (not ((self._in_neg[fr]) and (not self._in_neg[to]))) and (edge[2] + self.potential[fr] - self.potential[to] < 0):
          if cost_now > edge[2] + self.potential[fr] - self.potential[to]:
            target = edge
            cost_now = edge[2] + self.potential[fr] - self.potential[to]
          #return edge
      if target is not None:
        return target
  
  def _find_tree_path(self, v): # 頂点vから親へのパス
    path = []
    now_v = v
    while self.prv[now_v] is not None:
      next_edge = self.prv[now_v]
      path.append(next_edge)
      now_v = next_edge[1]
    return path
        
  def _find_flux_and_last_degenerate(self, path): # path上に流せる量と、それを流したときに退化する最後の辺を求める
    now_val = 1 << 60
    for edge in path:
      now_val = min(now_val, edge[3] - edge[0])
    for edge in path[::-1]:
      if edge[3] - edge[0] == now_val:
        return now_val, edge
  
  def __reculc_pot(self, v, vis):
    if vis[v]: return self.potential[v]
    prv_edge = self.prv[v]
    vis[v] = True
    if prv_edge is None:
      self.potential[v] = 0
      self._in_neg[v] = (self.balance[v] < 0)
      self._root[v] = v
    else:
      p = prv_edge[1]
      self.potential[v] = self.__reculc_pot(p, vis) - prv_edge[2]
      self._in_neg[v] =  self._in_neg[p]
      self._root[v] =  self._root[p]
    return self.potential[v]
    
  def _reculc_potential(self):
    vis = [False] * self.N
    for i in range(self.N):
      if vis[i]: continue
      self.__reculc_pot(i, vis)
    
  def find_flow(self, debug = False):
    c = 0
    while True:
      c += 1
      
      self._reculc_potential()
      target_edge = self._pick_edge()
      if target_edge is None:
        break
      
      if debug: 
        print("pivot {:}".format(c), "total_cost: {:}".format(self.total_cost))
        print(" target_edge : {:}".format(target_edge))
        for i in range(self.N):
          print(" vertex {:}: {:}".format(i, self.prv[i]))
        print(" potential", self.potential)
        print(" balance", self.balance)
        print(" root", self._root)
        print(" in_neg", self._in_neg)
      
      fr = target_edge[-1][1]
      to = target_edge[1]
      path_fr = self._find_tree_path(fr)
      path_to = self._find_tree_path(to)
        
      # 重複除去
      while path_fr and path_to and (path_fr[-1] is path_to[-1]):
        path_fr.pop()
        path_to.pop()
        
      par_fr = path_fr[-1][1] if path_fr else fr # fr側の親
      par_to = path_to[-1][1] if path_to else to # to側の親
      # 木間の辺か否か
      is_inter = (par_fr != par_to)
      
      path = [edge[-1] for edge in path_fr[::-1]] + [target_edge] + path_to
      
      
      max_flux, removing_edge = self._find_flux_and_last_degenerate(path)
      rev_flag = False
      if is_inter:
        a_flag = False
        if self.balance[par_to] <= 0:
          max_flux = min(max_flux, -self.balance[par_to])
        if 0 <= self.balance[par_fr] < max_flux:
          a_flag = True
          max_flux = max(0, self.balance[par_fr])
          
        if self.balance[par_to] <= 0 and -self.balance[par_to] == max_flux:
          rev_flag = True
          removing_edge = None
        if a_flag: # 0 <= self.balance[par_fr] < max_flux and self.balance[par_fr] == max_flux:
          removing_edge = None
          
        self.balance[par_to] += max_flux
        self.balance[par_fr] -= max_flux
      
      for edge in path[::-1]:
        edge[0] += max_flux
        edge[-1][0] -= max_flux
        if edge is removing_edge:
          rev_flag = True
        elif not rev_flag:
          self.prv[edge[-1][1]] = edge
        else:
          self.prv[edge[1]] = edge[-1]
        
      self.total_cost += max_flux * (target_edge[2] + self.potential[fr] - self.potential[to]) 
      
      # ポテンシャルの計算は次のループの最初で行う
  
  def add_vertex(self, b = 0):
    self.N += 1
    self.B.append(b)
    self.balance.append(b)
    self.potential.append(0)
    self.prv.append(None)
    self._in_neg.append(b < 0)
    self._root.append(self.N-1)
    self.I.append([])
  
  def set_vertex(self, v, b_new = 0):
    b_prv = self.B[v]
    if b_new == b_prv: return
    self.B[v] = b_new
    self.balance[v] += b_new - b_prv
    
  def add_edge(self, fr, to, cost, cap, low = 0):
    flux = min(cap, max(0, low))
    self.total_cost += flux * cost
    
    edge = [flux, to, cost, cap, None]
    rev = [-flux, fr, -cost, -low, edge]
    edge[-1] = rev
    self.edges.append(edge)
    self.edges.append(rev)
    self.I[fr].append(edge)
    self.I[to].append(rev)
      
    if flux != 0:
      self.balance[fr] -= flux
      self.balance[to] += flux
      self.prv[fr] = None
      self.prv[to] = None
      
    
  def set_edge(self, edge_id, cost_new, cap_new, low_new = 0):
    edge = self.edges[edge_id << 1]
    rev = edge[-1]
    self.total_cost -= edge[0] * edge[2]
    
    flux_new = min(max(edge[0], low_new), cap_new)
    flux_diff = flux_new - edge[0]
    
    if flux_diff != 0:
      self.balance[rev[1]] -= flux_diff # fr
      self.balance[edge[1]] += flux_diff # to
      self.prv[fr] = None
      self.prv[to] = None
      
    edge[0] = flux_new
    rev[0] = -flux_new
    edge[2] = cost_new
    rev[2] = -cost_new
    edge[3] = cap_new
    rev[3] = -low_new
      
    self.total_cost += edge[0] * edge[2]
    
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
