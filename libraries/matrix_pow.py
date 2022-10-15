def mat_mal(P, Q, mod = 0):
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

def inv_mal(P):
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

def inv_mal_mod(P, mod): # modありの逆行列を求める。inv(x, mod)をnumbersからインポートすること
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
