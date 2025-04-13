# 行列P * 行列Q 
def mat_mul(P, Q, mod = 0):
  a = len(P)
  c = len(P[0])
  b = len(Q[0])
  R = []
  for i in range(a):
    r0 = []
    for j in range(b):
      tmp = 0
      for k in range(c):
        tmp += P[i][k] * Q[k][j]
        if mod:
          tmp %= mod
      r0.append(tmp)
    R.append(r0)
  return R

# 行列累乗 (P ^ N)
def mat_pow(P, N, mod = 0):
    P_pow = [P]
    for _ in range(N.bit_length() + 1):
        P_pow.append(mat_mul(P_pow[-1], P_pow[-1], mod))
    ans = [[int(i == j) for j in range(len(P))] for i in range(len(P))]
    j = 0
    NN = N
    while NN > 0:
        if NN & 1:
            ans = mat_mul(ans, P_pow[j], mod)
        NN >>= 1
        j += 1
    return ans

# 行列P * ベクトルv
def mat_vec_mul(P, v, mod = 0):
  if len(P[0]) != len(v):
    return None
  
  ans = []
  for i in range(len(P)):
    tmp = 0
    for j in range(len(v)):
      tmp += P[i][j] * v[j]
      if mod: tmp %= mod
      
    ans.append(tmp)
    
  return ans

# 行列Pの逆行列
def inv_mat(P):
  a = len(P)
  Q = [[int(i == j) for j in range(a)] for i in range(a)]
  for i in range(a):
    flag = False
    for j in range(i, a):
      if abs(P[j][i]) > 10 ** (-8):
        piv = P[j][i]
        for k in range(a):
          P[j][k] /= piv
          Q[j][k] /= piv
        for l in range(a):
          if l == j: continue
          piv2 = P[l][i]
          #print(i, l, j, piv2)
          for k in range(a):
            P[l][k] -= piv2 * P[j][k]
            Q[l][k] -= piv2 * Q[j][k]
      flag = True
      break
      P[j], P[i] = P[i], P[j]
      Q[j], Q[i] = Q[i], Q[j]
      
    if not flag:
      return None # ランク落ち
    
  return Q

mod = 998244353
# mod = 素数
_inv_t = {}
_inv_t[1] = 1
_inv_t[0] = 0
def inv(x, mod):
  x %= mod
  if x not in _inv_t:
    _inv_t[x] = inv(mod % x, mod) * (mod - mod // x) % mod
  return _inv_t[x]

def inv_mat_mod(P, mod): # modありの逆行列を求める。inv(x, mod)をnumbersからインポートすること
  a = len(P)
  Q = [[int(i == j) for j in range(a)] for i in range(a)]
  for i in range(a):
    flag = False
    for j in range(i, a):
      if not P[j][i]:
        piv = P[j][i]
        for k in range(a):
          P[j][k] *= inv(piv, mod)
          P[j][k] %= mod
          Q[j][k] *= inv(piv, mod)
          Q[j][k] %= mod
        for l in range(a):
          if l == j: continue
          piv2 = P[l][i]
          for k in range(a):
            P[l][k] = (P[l][k] - piv2 * P[j][k]) % mod
            Q[l][k] = (Q[l][k] - piv2 * Q[j][k]) % mod
      flag = True
      break
      P[j], P[i] = P[i], P[j]
      Q[j], Q[i] = Q[i], Q[j]
      
    if not flag:
      return None # ランク落ち
    
  return Q

# 行列の掃き出し(できるだけ上に寄せる)
# 同時に行列式を求める。O(N^3)
def sweep_mat(A, mod = 0):
  n = len(A)
  if n != len(A[0]):
    return None
  
  det = 1 # 行列式
  
  A = [[v for v in a] for a in A]
  i_done = 0
  for j in range(n):
    target_i = -1
    for k in range(i_done, n):
      if A[k][j] != 0:
        target_i = k
        break
        
    if target_i == -1: # all 0
      continue
      
    v = A[target_i][j]
    v_inv = inv(v, mod) if mod else 1 / v
    
    det *= v
    if mod: det %= mod
    
    for l in range(j, n):
      A[target_i][l] *= v_inv
      if mod: A[target_i][l] %= mod
      
    for i in range(n):
      if i == target_i: continue
      a = A[i][j]
      for l in range(j, n):
        A[i][l] -= A[target_i][l] * a
        if mod: A[i][l] %= mod
          
    if target_i != i_done:
      A[target_i], A[i_done] = A[i_done], A[target_i]
      det *= -1
    i_done += 1
    
  return A, det

def sweep_on_F2(A): # 掃き出し法(@F2)
  N = len(A)
  M = len(A[0])
  now = -1
  rank = N
  for i in range(M):
    v = -1
    for j in range(now + 1, N):
      if A[j][i] != 0:
        v = j
        break
    if v == -1:
      rank -= 1
      continue
    #print(v)
    A[v], A[now+1] = A[now+1], A[v]
    now += 1
    for j in range(N):
      if A[j][i] == 0 or j == now: continue
      for k in range(M):
        A[j][k] ^= A[now][k]
  return A, rank

def solve_simultaneous_equations_on_F2(A): # Aは掃き出された行列(@F2)。連立方程式の解を求める
  N = len(A)
  M = len(A[0])
  V = [[] for _ in range(M)]
  head = set()
  for a in A:
    flag = -1
    ct = 0
    #print(a)
    for i, v in enumerate(a):
      if v == 0: continue
      if flag == -1:
        flag = i
        head.add(flag)
        #print(i)
      else:
        V[i].append(flag)
        ct += 1
  
  base = []
  for i in range(M):
    if i in head: continue
    tmp = [0] * M
    tmp[i] = 1
    for j in V[i]:
      tmp[j] = 1
    base.append(tmp)
        
  return base
