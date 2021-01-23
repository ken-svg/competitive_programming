# Primal Dual
from heapq import heapify, heappop, heappush
class mincostflow():
  def __init__(self, n):
    self.n = n
    self.edge_num = 0
    self.edges = []
    self.G = [[] for i in range(n)]
    
  def add_edge(self, fr, to, cap, cost, cap_rev = 0): # 辺を追加
    # fr: 始点, to: 終点, cap: 容量, cost: 1流量あたりの費用, cap_rev = 逆辺容量（すなわち初期流量）
    edge_num = self.edge_num
    forward = [cap, cost, to, None, edge_num<<1]
    forward[3] = backward = [cap_rev, -cost, fr, forward, (edge_num<<1) + 1] 
    self.edges.append(forward)
    self.edges.append(backward)
    self.edge_num += 1
    # 辺の持ち方: [残り容量, 費用, 行き先, 相互参照, 辺番号]
    self.G[fr].append(forward)
    self.G[to].append(backward)
    
  def reset(self): # 流量をリセット
    edges = self.edges
    for e_id in range(0, self.edge_num<<1, 2):
      edges[e_id][0] += edges[e_id+1][0]
      edges[e_id+1][0] = 0
    
  def _Dijkstra(self, s, t, flow_limit = 1<<60): 
    # 始点sから各点への最短路を計算し、めいいっぱいフローを流す
    G = self.G
    pot = self.potential # ポテンシャル
    INF = 1<<60
    
    dist = [-1]*self.n # 各点までの距離
    path = [None]*self.n # 各点の直前に通るべき辺の番号
    
    task = [s] # heapq
    vis = [False]*self.n # すでに最短距離が確定した場合 True
    while task:
      x = heappop(task)
      
      y, fr = x // INF, x % INF
      c, e_id = y // INF, y % INF
      
      if vis[fr]: continue
      path[fr] = e_id
      dist[fr] = c
      vis[fr] = True
      
      for cap, cost, to, _, e_id in G[fr]:
        if vis[to] or cap == 0: continue
        c_next = c + cost - (pot[to] - pot[fr])
        heappush(task, (c_next * INF + e_id) * INF + to)
      
    # ポテンシャルの更新
    for i in range(self.n):
      if dist[i] == -1: continue
      pot[i] += dist[i]
    
    # フローを実行
    edges = self.edges
    if path[t] == None: return -1, -1
    to = t
    add_flow = flow_limit
    add_cost = 0
    modified = []
    while to != s:
      edge = edges[path[to]]
      rev_edge = edge[3]
      add_flow = min(add_flow, edge[0])
      add_cost += edge[1]
      to = rev_edge[2]
      modified.append(edge)
      
    for edge in modified:
      rev_edge = edge[3]
      edge[0] -= add_flow
      rev_edge[0] += add_flow
        
    return add_flow, add_cost * add_flow # 流量増分, コスト増分
  
  def min_cost_max_flow(self, s, t, flow_limit = 1<<60):
    self.potential = [0]*self.n
    self.reset()
    
    flow, cost = 0, 0
    while True:
      af, ac = self._Dijkstra(s, t, flow_limit-flow)
      if af == -1: return flow, cost
      flow += af
      cost += ac
      if flow == flow_limit: return flow, cost
    return flow, cost
        
  def min_cost_slope(self, s, t, flow_limit = 1<<60):
    self.potential = [0]*self.n
    self.reset()
    
    ans = [[0,0]]
    flow, cost = 0, 0
    while True:
      af, ac = self._Dijkstra(s, t, flow_limit-flow)
      if af == -1: return ans
      flow += af
      cost += ac
      ans.append([flow,cost])
      if flow == flow_limit: return ans
    return ans
    
  def get_edge(self, edge_idx): # 辺番号 edge_idx の辺の状態を取得する
    if 0 <= edge_idx < self.edge_num:
      cap, cost, to, rev_edge, _ = self.edges[edge_idx<<1]
      now_flow, _, fr, _, _ = rev_edge
      return {"cap": cap, "flow": now_flow, "from": fr, "to": to, "cost": cost}
    else:
      return
    
  def get_edges(self): # 全ての辺の状態を取得する
    ans = [None]*self.edge_num
    for cap, cost, to, rev_edge, e_id in self.edges[::2]:
      now_flow, _, fr, _, _ = rev_edge
      ans[e_id>>1] = {"cap": cap, "flow": now_flow, "from": fr, "to": to, "cost": cost}
    return ans
    
    
# method 一覧
# def add_edge(fr, to, cap, cost, cap_rev = 0): frからtoへ容量cap, コストcostの辺を張る。cap_revは逆辺の初期容量。
# def reset(): # 全ての辺を残したまま、流量をリセットする
# def min_cost_max_flow(s, t, flow_limit = 1<<60): sからtまでフローを流し、最大流量およびそのときのコストを返す。flow_limitが指定されている場合、その流量以下最大の流量を達成するフローを流し、流量とコストを返す。
# def min_cost_slope(s, t, flow_limit = 1<<60): sからtまでフローを流し、各流量における最小コストを返す（内部のフローは最大フローとなる）
# get_edge(edge_idx): 辺番号edge_idxの辺の状態を返す。{"cap": 残り容量, "flow": 現在流量, "from": 始点, "to": 終点, "cost": 辺のコスト}の辞書を返す。
# get_edges(): 全ての辺について、上記形式の辞書を返す。
