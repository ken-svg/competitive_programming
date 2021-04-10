# Dijkstra法(グラフが隣接リストで与えられる場合)
from heapq import heappush, heappop
# s: 始点, I: 隣接リスト -> cost: sから各点の距離(リスト)
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
