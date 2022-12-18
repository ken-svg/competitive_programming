def strongly_connected_component(I, N):
  vis = [False] * N
  # 1. 帰りがけ順の作成
  I_iter = [(i + [-2]).__iter__() for i in I]
  order = []
  for s in range(N):
    if vis[s]: continue
    vis[s] = True
    path = [[I_iter[s], s]]
    while path:
      p = path[-1][1]
      q = next(path[-1][0])
      if q == -2: # その点から先へはいけない
        order.append(p)
        path.pop()
      else:
        if vis[q]: continue
        path.append([I_iter[q], q])
        vis[q] = True
  # 2. 逆辺グラフ上で強連結成分を作成
  # https://manabitimes.jp/math/1250
  vis = [False] * N
  R = [[] for _ in range(N)]
  for i in range(N):
    for j in I[i]:
      R[j].append(i)
  ans_comp = []
  ans_comp_inv = [-1] * N
  comp_id = 0
  for v in order[::-1]:
    if vis[v]: continue
    vis[v] = True
    task = [v]
    comp_set = {v}
    ans_comp_inv[v] = comp_id
    while task:
      p = task.pop()
      for q in R[p]:
        if vis[q]:
          cq = ans_comp_inv[q]
        else:
          comp_set.add(q)
          ans_comp_inv[q] = comp_id
          task.append(q)
          vis[q] = True 
    ans_comp.append(comp_set)
    comp_id += 1
  ans_I = [set() for _ in range(comp_id)]
  for i in range(N):
    for j in I[i]:
      if ans_comp_inv[i] != ans_comp_inv[j]:
        ans_I[ans_comp_inv[i]].add(ans_comp_inv[j])
  return ans_comp, ans_comp_inv, ans_I 
  # 成分(set), 頂点ごとの所属成分, 成分間の隣接リスト 

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

class Two_SAT():
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
  
  def is_possible(self): # 充足可能かどうかを返す
    I = self.I
    C, C_inv, Ir = strongly_connected_component(I, 2 * self.n)
    for i in range(self.n):
      if C_inv[i << 1] == C_inv[(i << 1) | 1]:
        return False  
    return True
    
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
