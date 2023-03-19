# Dijkstra法(グラフが隣接リストで与えられる場合)
from heapq import heappush, heappop
# s: 始点, I: 隣接リスト I[p]の要素は(隣接点q, コストc) -> cost: sから各点の距離(リスト)
def Dijkstra(s, I):
  INF = 10**30
  task = [(0, s)]
  cost = [INF]*N
  vis = [False]*N
  while task:
    c, p = heappop(task)
    if vis[p]: continue
    vis[p] = True
    cost[p] = c
    for q, c0 in I[p]:
      if vis[q]: continue
      heappush(task,(c + c0, q))
      
  return cost




# 一般グラフno最大マッチング(ネタ枠w)
# 計算量 0(EVlogE)らしい
# 参考にした解説： https://qiita.com/Kutimoti_T/items/5b579773e0a24d650bdf
from collections import deque
import sys
sys.setrecursionlimit(10 ** 6)
def genaral_maximum_matching(I): # 0-indexed adjacent list
  
  N = len(I)
  M = 0
  vis = set()
  
  # convert 0-index to 1-index and label edges
  I_conv = [[] for _ in range(N+1)]
  for i in range(N):
    for j in I[i]:
      if (j, i) in vis: continue
      vis.add((i, j))
      M += 1
      I_conv[i+1].append([j+1, M])
      I_conv[j+1].append([i+1, M])
  
  I = I_conv
  # prepare edge information 
  edge_info = [None] * (M + 1)
  for i in range(N):
    for j, e_id in I[i]:
      if edge_info[e_id] is None:
        edge_info[e_id] = [i, j]
  
  # E0
  label = [-1] * (N + 1)
  mate = [0] * (N + 1)
  first = [None] * (N + 1)
  
  # define subroutines
  def R(x, y): # u -> ... -> x(outer) -> y(unmatched) に沿ってaugument
    # R1
    t = mate[x]
    mate[x] = y
    if mate[t] != x: return
    
    # R2
    if label[x] <= N:
      mate[t] = label[x]
      R(label[x], t)
    
    # R3
    else:
      e_id = label[x] - N
      x = edge_info[e_id][0]
      y = edge_info[e_id][1]
      R(x, y)
      R(y, x)
  
  def eval_first(x):
    if label[first[x]] < 0:
      return first[x]
    first[x] = eval_first(first[x])
    return first[x]
    
  def L(x, y, e_id):
    # L0
    r = eval_first(x)
    s = eval_first(y)
    join = 0
    if (r == s):
      return
    
    num_e_id = e_id + N
    # flag
    label[r] = -num_e_id
    label[s] = -num_e_id
    while True:
      # L1
      if (s != 0):
        r, s = s, r
        
      # L2
      r = eval_first(label[mate[r]])
      if label[r] == -num_e_id:
        join = r
        break
      label[r] = -num_e_id
      
    # L3
    v = first[x]
    # L4
    while (v != join):
      Q.append(v)
      label[v] = num_e_id
      first[v] = join
      v = first[label[mate[v]]]
      
    # L3
    v = first[y]
    # L4
    while (v != join):
      Q.append(v)
      label[v] = num_e_id
      first[v] = join
      v = first[label[mate[v]]]
    
    # L6
    return
      
  
  # E1 to E7
  for u in range(1, N+1):
    # E1
    if mate[u] != 0: continue
    
    label[u] = 0
    first[u] = 0
    Q = deque([u])
    
    E7_flag = False
    while Q:
      # E2
      if not Q: continue # -> E1
      x = Q.popleft()
      for y, e_id in I[x]:
        # E3
        if mate[y] == 0 and y != u:
          mate[y] = x # マッチング
          R(x, y) # パスに沿った拡大
          # -> R7(break?)
          E7_flag = True
          break

        # E4
        elif label[y] >= 0: # y is outer:
          L(x, y, e_id)

        # E5
        elif label[mate[y]] < 0: #mate[y] is non-outer
          my = mate[y]
          label[my] = x
          first[my] = y
          Q.append(my)

        # E6
        continue
        
      if E7_flag: break
        
    # E7
    if E7_flag:
      label = [-1] * (N + 1)
      
  ans = [mate[i+1] - 1 for i in range(N)]
  return ans
