# 問題文
# https://atcoder.jp/contests/typical90/tasks/typical90_ai
# ・非再帰でオイラーツアー
# ・ついでにLCA(最近祖先)

N = int(input())
I = [[] for _ in range(N)]

for _ in range(N-1):
  a, b = map(int,input().split())
  a -= 1
  b -= 1
  I[a].append(b)
  I[b].append(a)

#print(I)  
def tree(s):
  Ir = [[] for _ in range(N)]
  depth = [0]*N
  task = [s]
  vis = [False]*N
  vis[s] = True
  while task:
    p = task.pop()
    d_p = depth[p]
    for q in I[p]:
      if vis[q]: continue
      Ir[p].append(q)
      task.append(q)
      vis[q] = True
      depth[q] = d_p + 1
    
  return Ir, depth

Ir, depth = tree(s = 0)
#print(Ir, depth)

Q = int(input())
que = [[] for _ in range(N)]
for i in range(Q):
  V = list(map(int,input().split()))
  for v in V[1:]:
    que[v-1].append(i)
  
#print(que)
INF = 10**10
ans = [0]*Q
depth_min = [INF]*Q
latest_point = [-1]*Q

# ここからLCAを求める操作(木の隣接リストをIrとする。)
par0 = [-1]*N
for i in range(N):
  for j in Ir[i]:
    par0[j] = i
par = [par0]
for _ in range(N.bit_length()+1):
  par_last = par[-1]
  par_next = [-1]*N
  for i in range(N):
    par_next[i] = par_last[par_last[i] if par_last[i] >= 0 else -1]
  par.append(par_next)
def LCA(p, q):
  if depth[p] < depth[q]:
    p, q = q, p
  dif = depth[p] - depth[q]
  idx = 0
  while dif > 0: # 深さを揃える
    if dif & 1:
      p = par[idx][p]
    dif >>= 1
    idx += 1
  if p == q: return p
  idx = len(par)-1
  while idx >= 0:
    par_now = par[idx]
    if par_now[p] != par_now[q]:
      p = par_now[p]
      q = par_now[q]
    idx -= 1
  par0 = par[0]
  return par0[p]
# LCAここまで

# 非再帰dfs
def dfs(s):
  path = [(-1, s)]
  piv = [0]*N # 何番目の辺まで調べたか
  # vis = [False]*N 木でない場合は必要
  q = 0
  p = s
  start = False
  while path:
    if piv[p] == 0: 
      # 行きがけ処理
      # vis[p] = True
      None 
      
    if piv[p] == len(Ir[p]):
      # 帰りがけ処理
      d_p = depth[p]
      for q_id in que[p]:
        if latest_point[q_id] != -1: #すでにそのクエリに１点以上見つかっている場合
          p_p = latest_point[q_id]
          lca = LCA(p, p_p)
          if depth_min[q_id] < depth[lca]:
            ans[q_id] += d_p - depth[lca]
          else:
            ans[q_id] += d_p - depth[lca] + depth_min[q_id] - depth[lca]
            depth_min[q_id] = depth[lca]
        else:
          depth_min[q_id] = d_p
        latest_point[q_id] = p
        
        
      path.pop()
      if path: 
        q, p = path[-1]
    else:
      #if not vis[p]: (２行インデント)
      q, p = p, Ir[p][piv[p]]
      path.append((q, p))
      piv[q] += 1
      # else: (１行インデント)
      # piv[p] += 1
      
      
    #print(q, p, path, ans, latest_point)
  return ans
print(*dfs(s=0), sep="\n")      
    
  
