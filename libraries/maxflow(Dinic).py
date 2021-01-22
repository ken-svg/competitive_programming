# Dinic
from collections import deque
class maxflow:
  def __init__(self, n):
    self.n = n
    self.G = [[] for i in range(n)] # 隣接グラフ
    self.edges = []
    self.edge_num = 0
    self.flow_now = 0
    self.start = None
    self.terminal = None
    
  def add_edge(self, fr, to, cap, cap_rev = 0): # 辺を追加
    # fr: 始点, to: 終点, cap: 容量, cap_rev = 逆辺容量（すなわち初期流量）
    edge_num = self.edge_num
    forward = [cap, to, None, edge_num<<1]
    forward[2] = backward = [cap_rev, fr, forward, (edge_num<<1) + 1] 
    self.edges.append(forward)
    self.edges.append(backward)
    self.edge_num += 1
    # 辺の持ち方: [残り容量, 行き先, 相互参照, 辺番号]
    self.G[fr].append(forward)
    self.G[to].append(backward)
    
  def reset(self): # 流量をリセット
    edges = self.edges
    for e_id in range(0, self.edge_num<<1, 2):
      edges[e_id][0] += edges[e_id+1][0]
      edges[e_id+1][0] = 0
    self.flow_prv = self.flow_now
    self.flow_now = 0
    
  def _bfs(self, s, t): # 始点sから各点への最短距離(self.dis)を計算
    dist = self._dist = [-1]*self.n
    G = self.G
    task = deque([s])
    dist[s] = 0
    while task:
      p = task.popleft(); d_p = dist[p];
      d_n = d_p + 1
      for cap, q, _, _ in G[p]:
        if cap == 0 or dist[q] >= 0: continue
        dist[q] = d_n
        task.append(q)
    return dist[t] >= 0
    
  def _dfs(self, s, t, flow_limit):
    dist = self._dist
    it = self._it = [0]*self.n
    G = self.G
    dist_t = dist[t]
    path = [None]*dist_t # 今まで辿った経路を入れる（逆辺で管理）
    cap_min = [None]*dist_t+[10**20] # 今の経路において、各深さまでの容量最小値
    path_len_now = 0 
    ans = 0
      
    p = s
    while True:
      if ans == flow_limit: break # 流量上限がある場合、上限に達したら終了
      
      if it[p] == len(G[p]): # 全ての辺を見終わっているとき
        if p == s: break # 始点を見終わっているなら終了
        path_len_now -= 1
        p = path[path_len_now][1] # 前の辺を伝って戻る(pathには逆辺が入っていることに注意)
        it[p] += 1 # 次回はこの辺を調べないように
        continue
          
      cap, to, rev_edge, _ = next_edge = G[p][it[p]]
      #print(" next_edge :", next_edge, "depth :", dist[p], "->", dist[to])
      # 容量がないか、最短路でないか、tまでたどり着けないことが明らかのとき
      if cap == 0 or (dist[p] >= dist[to]) or (to != t and dist[p] == dist_t-1): 
        it[p] += 1
        continue
        
      # それ以外の場合は進行可能
      cap_min[path_len_now] = min(cap, cap_min[path_len_now-1])
      path[path_len_now] = rev_edge # 逆辺をpathに追加
      path_len_now += 1
      p = to
      if to != t: continue
        
      # 終点にたどり着いた時、フローを流す
      flow = min(flow_limit - ans, min(cap_min))
      q = t
      for d in range(dist_t-1,-1,-1):
        _, fr, edge, _ = rev_edge = path[d]
        cap = edge[0]
        if cap == flow: # このフローによって容量が尽きるとき
          it[fr] += 1 # 次回はこの辺を調べないように
          path_len_now = d # pathをこの位置まで戻す
          p = fr
        #フローをこの辺に流す
        cap_min[d] -= flow
        edge[0] -= flow
        rev_edge[0] += flow
        q = fr
      ans += flow
    return ans

  def flow(self, s, t, flow_limit = 10**20): # sからtへの最大流量を計算、O(V^2 E)　(flow_limit: 流量上限)
    if self.start != s or self.tarminal != t:
      self.reset()
      self.start = s; self.terminal = t;
    bfs = self._bfs
    dfs = self._dfs
    ans = 0
    while bfs(s, t):
      self.flow_now += dfs(s, t, flow_limit)
    return self.flow_now # 上限以内で流せた流量を返す
  
  def min_cut(self, s): # 現在のフローにの残余グラフについて、sから行ける点をTrueで返す
    self._bfs(s, t=-1)
    return [a >= 0 for a in self._dist]
  
  def get_edge(self, edge_idx): # 辺番号 edge_idx の辺の状態を取得する
    if 0 <= edge_idx < self.edge_num:
      cap, to, rev_edge, _ = self.edges[edge_idx<<1]
      now_flow, fr, _, _ = rev_edge
      return {"cap": cap, "flow": now_flow, "from": fr, "to": to}
    else:
      return
    
  def get_edges(self): # 全ての辺の状態を取得する
    ans = [None]*self.edge_num
    for cap, to, rev_edge, e_id in self.edges[::2]:
      now_flow, fr, _, _ = rev_edge
      ans[e_id>>1] = {"cap": cap, "flow": now_flow, "from": fr, "to": to}
    return ans

# method 一覧
# def add_edge(fr, to, cap, cap_rev = 0): frからtoへ容量capの辺を張る。cap_revは逆辺の初期容量。
# def reset(): # 全ての辺を残したまま、流量をリセットする
# def flow(s, t, flow_limit = 10**20): sからtまでフローを流し、最大流量を返す。flow_limitが指定されている場合、その流量以下最大の流量を達成するフローを流し、流量を返す。
# def min_cut(s): 現在のフローの残余グラフ上で、点sから行ける点をTrue, いけない点をFalseで返す
# get_edge(edge_idx): 辺番号edge_idxの辺の状態を返す。{"cap": 残り容量, "flow": 現在流量, "from": 始点, "to": 終点}の辞書を返す。
# get_edges(): 全ての辺について、上記形式の辞書を返す。
