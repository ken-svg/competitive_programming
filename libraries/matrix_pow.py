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
