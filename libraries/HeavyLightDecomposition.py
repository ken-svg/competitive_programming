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

# shallowest: その点が属するHeavy pathの最も浅い点
# parent: sを根としたときの各点の親
# v_id: sを根とし、Heavy pathになじむような行き掛け順で頂点番号を振り直したもの（パスクエリをセグ木などに載せるときのインデックスとして使う）
# パスクエリをO(Nlog^2N)で処理。O(NlogN)の実装があるらしい・・・？！
