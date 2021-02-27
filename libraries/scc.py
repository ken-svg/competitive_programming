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


# おまけ(トポロジカルソート)
# !!verify前!!
def topological_sort(I): # 入力  I: 隣接リスト(DAG),  出力: top_order(list[int]) 
  N = len(I)
  in_deg = [0]*N # 入次数
  for i in range(N):
    for j in I[i]:
      in_deg[j] += 1
  print(in_deg)
  top_order = []
  vis = [False]*N
  for s in range(N):
    if vis[s] or in_deg[s] > 0: continue
    task = [s]
    vis[s] = True
    while task:
      i = task.pop()
      top_order.append(i)
      for j in I[i]: # 各出辺について
        if vis[j]: continue
        in_deg[j] -= 1 # 辺を取り除く
        if in_deg[j] > 0: continue # 入次数が残っているなら後回し
        vis[j] = True
        task.append(j)
        
  return top_order
