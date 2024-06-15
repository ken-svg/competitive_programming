def HeavyLightDecomposition(I, s):
  N = len(I)
  
  # DFS順の作成
  parent = [-1] * N
  vis = [False] * N
  order = []
  task = [s]
  while task:
    p = task.pop()
    vis[p] = True
    order.append(p)
    for q in I[p]:
      if vis[q]: continue
      parent[q] = p
      task.append(q)
  
  # subsize,weightの作成, heavy edgeの選択
  subsize = [0] * N
  weight = [0] * N
  #heavy = [-1] * N
  order.reverse()
  for p in order:
    c = 1
    max_size = -1
    #arg_max = -1
    heavy_index = -1
    for i, q in enumerate(I[p]):
      if q is parent[p]: continue
      sq = subsize[q]
      c += sq
      if sq > max_size:
        max_size = sq
        #arg_max = sq
        heavy_index = i
    subsize[p] = c
    if heavy_index != -1:
      Ip = I[p]
      Ip[-1], Ip[heavy_index] = Ip[heavy_index], Ip[-1] # heavy edgeをI[p]の最後尾に
      #heavy[p] = arg_max
      weight[p] = c - subsize[Ip[-1]]
    else:
      weight[p] = 0
        
  # 再度DFS順の作成(heavy edgeを最後尾に置いたため、これでseg木に並べる順が完成)
  # のちに部分木クエリに対応できるような順番にする
  order = []
  shallowest = [-1] * N
  task = [[s, -1]]
  while task:
    p, l = task.pop()
    if l == -1:
      l = p
    shallowest[p] = l
    order.append(p)
    upd_flag = False
    for q in I[p]:
      if q is parent[p]: continue
      upd_flag = True
      task.append([q, -1])
    if upd_flag: task[-1][1] = l # shallowestをheavy edgeの子へ受け継ぐ
  
  v_id = [-1] * N
  for i, v in enumerate(order):
    v_id[v] = i
    
  return shallowest, parent, v_id

# shallowest: その点が属するHeavy pathの最も浅い点
# parent: sを根としたときの各点の親
# v_id: sを根とし、Heavy pathになじむような行き掛け順で頂点番号を振り直したもの（パスクエリをセグ木などに載せるときのインデックスとして使う）
# パスクエリをO(Nlog^2N)で処理。O(NlogN)の実装があるらしい・・・？！


  
import sys
sys.setrecursionlimit(10 ** 6)
import pypyjit
pypyjit.set_param('max_unroll_recursion=-1')
def HeavyLightDecomposition(I, s):
  N = len(I)
  vis = [False] * N
  heavy = [-1] * N
  parent = [-1] * N
  def dfs_heavy_edge(p):
    vis[p] = True
    w_total = 1
    arg_max = -1
    max_val = -1
    for q in I[p]:
      if vis[q]: continue
      parent[q] = p
      w = dfs_heavy_edge(q)
      w_total += w
      if w > max_val:
        arg_max = q
        max_val = w
    heavy[p] = arg_max
    return w_total
  dfs_heavy_edge(s)
  vis = [False] * N
  v_id = [-1] * N
  shallowest = [-1] * N
  def dfs_decomposition(p, s, c, n):
    vis[p] = True
    v_id[p] = n
    n += 1
    if s == -1:
      s = p
    shallowest[p] = s
    h = heavy[p]
    if h != -1:
      c, n = dfs_decomposition(h, s, c, n)
    for q in I[p]:
      if vis[q]: continue
      c += 1
      c, n = dfs_decomposition(q, -1, c, n)
    return c, n
  dfs_decomposition(s, -1, 0, 0)  
  return shallowest, parent, v_id

