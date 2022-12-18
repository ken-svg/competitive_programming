# SCC(強連結成分分解)
def strongly_connected_component(I, N): 
  # 入力  I: 隣接リスト
  # 出力　points: 各成分に含まれる点(list[list[int]]]), Ir: 成分間の隣接リスト(list[set[int]])
  N = len(I) # 頂点数
  
  # 1, 帰りがけ順の作成(非再帰DFS) -> order(list[int])
  order = []
  par = [-1]*N
  next_task = [0 for _ in range(N)]
  vis = [False]*N
  for s in range(N):
    if vis[s]: continue
    task = [s]
    p = s
    vis[s] = True
    while p >= 0: # p = -1となるまで続ける
      task_idx = next_task[p]
      task_num = len(I[p])
      while task_idx < task_num:
        p_n = I[p][task_idx]
        if not vis[p_n]:
          break
        task_idx += 1

      if task_idx == task_num: # 全ての辺を調べ終わった時
        order.append(p) # 順番に加える（=帰りがけ順）
        p = par[p] # 親に戻る
        continue

      # そうでない時、p_nに進む
      par[p_n] = p
      vis[p_n] = True
      next_task[p] = task_idx + 1 # 次回のため、次の辺を指しておく
      p = p_n
      
  
  # 2, 強連結成分への分解
  rep = [-1]*N # 各成分の代表元
  R = [[] for _ in range(N)] # 逆グラフの作成
  for i in range(N):
    for j in I[i]:
      R[j].append(i)
  order.reverse()
  vis = [False]*N
  reps = [] # 代表元集合
  for r in order:
    if vis[r]: continue
    rep[r] = r
    vis[r] = True
    reps.append(r)
    # 逆グラフ上でrから到達できる点を列挙
    task = [r]
    while task:
      p = task.pop()
      for q in R[p]:
        if vis[q]: continue
        vis[q] = True
        rep[q] = r
        task.append(q)
        
  reps_inv = [-1]*N
  for i, r in enumerate(reps):
    reps_inv[r] = i
    
  Nr = len(reps)
  Ir = [set() for _ in range(Nr)] # 簡約後の隣接リスト
  for i in range(N):
    ir = reps_inv[rep[i]]
    for j in I[i]:
      jr = reps_inv[rep[j]]
      if ir == jr: continue
      Ir[ir].add(jr) 
  points = [set() for _ in range(Nr)]
  for i in range(N):
    points[reps_inv[rep[i]]].add(i)
  points_inv = [-1] * N
  for i, s in enumerate(points):
    for j in s:
      points_inv[j] = i
  
  return points, points_inv, Ir # 各成分に含まれる点(list[list[int]]]), 成分間の隣接リスト(list[set[int]])

from collections import deque
def topological_sort(I):
  N = len(I)
  task = deque([])
  vis = [False] * N 
  indeg = [0] * N
  for s in range(N):
    for p in I[s]:
      indeg[p] += 1
  for s in range(N):
    if indeg[s] == 0:
      task.append(s)
      vis[s] = True
  
  ans_order = []
  while task:
    p = task.popleft()
    ans_order.append(p)
    for q in I[p]:
      if vis[q]: continue
      indeg[q] -= 1
      if indeg[q] == 0:
        task.append(q)
        vis[q] = True
  return ans_order, (len(ans_order) == N) # DAGでない場合、二つ目の戻り値がFalseとなる

class Two_SAT(): # 2-SATを解く
  def __init__(self):
    self.n = 0
    self.I = []
    self.info = []
    
  def add(self, a, b, ta, tb): # (a != ta) -> (b == tb), (b != tb) -> (a == ta)
    I = self.I
    for _ in range((max(a, b) + 1) * 2 - len(self.I)):
      I.append([])   
    I[(b<<1) + (1 ^ int(tb))]
    I[(a<<1) + (1 ^ int(ta))].append((b<<1) + int(tb))    
    I[(b<<1) + (1 ^ int(tb))].append((a<<1) + int(ta))
    if a > b or (a == b and int(ta) > int(tb)):
      a, b = b, a
      ta, tb = tb, ta
      
    self.info.append([(a, ta), (b, tb)])
    self.n = len(I) // 2
    
  def derive(self): # 充足可能なら解の一つを返し、そうでにならNoneを返す
    I = self.I
    C, C_inv, Ir = strongly_connected_component(I, 2 * self.n)
    for i in range(self.n):
      if C_inv[i << 1] == C_inv[(i << 1) | 1]:
        return None  
    top_order_Ir = topological_sort(Ir)[0]
    TF = [-1] * self.n
    for comp_id in top_order_Ir:
      a0 = list(C[comp_id])[0]
      if TF[a0 >> 1] == -1:
        for a in C[comp_id]:
          TF[a >> 1] = (a & 1) ^ 1
          
    return [bool(tf) for tf in TF]
  
  def __str__(self):
    rtn = "<Two SAT on X_0 ~ X_{}> \n".format((self.n) - 1)
    self.info.sort()
    for (a, ta), (b, tb) in self.info:
      rtn += (" X_{}".format(a) if ta else "-X_{}".format(a)) + " ∨ " + (" X_{}".format(b) if tb else "-X_{}".format(b)) + "\n"
    return rtn[:-1] 
