import sys
import pypyjit
pypyjit.set_param('max_unroll_recursion=-1')
sys.setrecursionlimit(10 ** 6)
def lowlink(I):
  N = len(I)
  vis = [False] * N
  low = [-1] * N
  order = [-1] * N
  def dfs(p, pp, c):
    vis[p] = True
    order[p] = c
    l = c
    c += 1
    flag = False
    for q in I[p]:
      if pp == q and not flag:
        flag = True
        continue
      if vis[q]:
        l = min(l, order[q])
      else:
        c, l0 = dfs(q, p, c)
        l = min(l, l0)
    low[p] = l
    return c, l
  for p in range(N):
    if vis[p]: continue
    dfs(p, -1, 0)
  return order, low
  
def find_bridge(I, order, low):
  N = len(I)
  vis = [False] * N
  ans = []
  def dfs(p, pp):
    vis[p] = True
    flag = False
    for q in I[p]:
      if vis[q]: continue
      if low[q] > order[p]:
        ans.append([p, q])
      dfs(q, p)
  for p in range(N):
    if vis[p]: continue
    dfs(p, -1)
  return ans
