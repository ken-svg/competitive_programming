# SCC(強連結成分分解)

def strongly_connected_component(I): 
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
  points = [[] for _ in range(Nr)]
  for i in range(N):
    points[reps_inv[rep[i]]].append(i)
  
  return points, Ir # 各成分に含まれる点(list[list[int]]]), 成分間の隣接リスト(list[set[int]])
# 戻り値についての説明
# points は、強連結成分ごとに、所属する点の番号を列挙したもの。強連結成分の順番や成分内の列挙の順番は保証しない。
#  例)強連結成分が{0,3,4}, {1,5}, {2}なら、戻り値の一例は[[0,3,4], [1,5], [2]]。ただし、順序は逆転しうる。
# Ir は、強連結成分間の隣接リストを示す。強連結成分の番号は、pointsにおける列挙順。
#  例)強連結成分の隣接関係が{0,3,4}->{1,5}->{2}で、pointsとして[[0,3,4], [1,5], [2]]を返した場合、
#  　　　　　Ir = [[1], [2], []]となる。（成分0->成分1, 成分1->成分2であり、成分2からは辺が出ていないことを、Ir[0]=[1], Ir[1]=[2], Ir[2]=[]となるリストIrとして表している。)
#    　pointsにおける強連結成分の列挙順によって、同型なグラフでも、各強連結成分の番号の付け方が異なる場合のあることに注意。


# おまけ(トポロジカルソート)
from collections import deque
def topological_order(I):
  N = len(I)
  task = deque([])
  vis = [False] * N 
  indeg = [0] * ct
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
