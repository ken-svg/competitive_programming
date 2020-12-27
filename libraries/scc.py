# SCC(強連結成分分解)

def scc(I): # I:隣接リスト
  def dfs_sort(s):
    vis.add(s)
    for j in I[s]:
      if j in vis: continue
      dfs_sort(j)
    top.append(s)
  def dfs_mash(s, ct):
    vis.add(s)
    for j in R[s]:
      if j in vis: continue
      dfs_mash(j, ct)
    cts[s] = ct
  
  vis = set()
  top = [] # 帰りがけ順の作成
  for s in range(len(I)):
    if s in vis: continue
    dfs_sort(s)
  R = [set() for _ in range(len(I))] # 逆向きグラフ
  cts = [-1 for _ in range(len(I))]
  for i in range(len(I)):
    for j in I[i]:
      R[j].add(i)
  vis = set()
  ct = 0
  for s in top[::-1]:  # 強連結成分にまとめる、番号付け
    if s in vis: continue
    dfs_mash(s, ct)
    ct += 1
    
  Ir = [set() for _ in range(ct)]
  for i in range(len(I)):
    cts_i = cts[i]
    for j in I[i]:
      cts_j = cts[j]
      if cts_i == cts_j: continue
      Ir[cts_i].add(cts_j)
      
  return Ir, cts # Ir: 簡約されたグラフの隣接リスト（ループなし）、cts[i]:もとの頂点iが簡約後にどの強連結成分に属するか
  
# 用法：
# 入力：有向グラフの隣接リスト I[p] = set([pに隣接する点])
# 出力：簡約されたグラフの隣接リスト（ループなし）、もとの頂点が簡約後にどの強連結成分に属するかの情報
