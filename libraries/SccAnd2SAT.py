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


# 22/12/25 sccとは独立に実装します
# 使用例: https://atcoder.jp/contests/abc277/submissions/37578021
class Two_SAT():
  def __init__(self):
    self.I = []
    
  def add(self, a, b, ta, tb): # (a != ta) -> (b == tb), (b != tb) -> (a == ta)
    I = self.I
    for _ in range((max(a, b) + 1) * 2 - len(self.I)):
      I.append([])   
    I[(a<<1) | (1 ^ int(ta))].append((b<<1) | int(tb))    
    I[(b<<1) | (1 ^ int(tb))].append((a<<1) | int(ta))
  
  def infer(self, a, b, ta, tb):  # (a == ta) -> (b == tb), (b == tb) -> (a == ta)
    I = self.I
    for _ in range((max(a, b) + 1) * 2 - len(self.I)):
      I.append([])   
    I[(a<<1) | int(ta)].append((b<<1) | int(tb))    
    I[(b<<1) | (1 ^ int(tb))].append((a<<1) | (1 ^ int(ta)))
  
  def derive(self, constraint = None):
    # constraintの与え方: [[Trueノード], [Falseノード]]
    I = self.I
    # 0) 拘束条件の処理
    if constraint == None:
      constraint = [[], []]
    true = len(I) | 1　 # constraintの処理のため、必ずTrueとなる頂点を追加する
    false = true ^ 1　
    I.append([]) # I[false]
    I.append([]) # I[true]
    for c in constraint[0]: # Trueノード
      #self.infer(true >> 1, c, True, True)
      I[true].append((c << 1) | 1)
      I[(c << 1)].append(false)
    for c in constraint[1]: # Falseノード
      #self.infer(true >> 1, c, True, False)
      I[true].append((c << 1))
      I[(c << 1) | 1].append(false)
    for i in range(false): # trueが最下位、falseが最上位に来るための処理
      #self.infer(i >> 1, true >> 1, i & 1, True)
      I[i].append(true)
      I[false].append(i ^ 1)
      
    # 1) 帰りがけ順をDFSにより決定
    N = len(I)
    order = []
    index_max = [len(i) for i in I]
    path = [false]
    index = [0] * N
    vis = [False] * N
    vis[false] = True
    while path:
      p = path[-1]
      if index[p] == index_max[p]:
        order.append(path.pop())
        continue
      q = I[p][index[p]]
      index[p] += 1
      if vis[q]: continue
      vis[q] = True
      path.append(q)
      
    #　2) 上流から順にTFを決定
    TF = [None] * N
    R = [[] for _ in range(N)]
    for i in range(N):
      for j in I[i]:
        R[j].append(i)
    for i in order[::-1]:
      if not vis[i]: continue
      vis[i] = False
      task = [i]
      comp = [i]
      while task:
        p = task.pop()
        for q in R[p]:
          if not vis[q]: continue
          vis[q] = False
          task.append(q)
          comp.append(q)
      # TFを確定
      if TF[i^1] == None: # 相方が未確定
        state = False
      else: # 相方が確定(Falseのはず)
        state = True
      for p in comp: # TFを確定させながら、相方との矛盾が生じないか判定
        if TF[p^1] != None and TF[p^1] == state: 
          return None # 充足不能
        TF[p] = state
    return TF[1:len(TF)-1:2]
