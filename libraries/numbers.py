# mod = 素数
mod = 998244353
_inv_t = {}
_inv_t[1] = 1
_inv_t[0] = 0
def inv(x, mod):
  x %= mod
  if x not in _inv_t:
    _inv_t[x] = inv(mod % x, mod) * (mod - mod // x) % mod
  return _inv_t[x]

# 約数列挙 O(\sqrt(N))
import math
def find_divisors(N):
  lim = math.floor(math.sqrt(N)+10**(-10))
  ans_l = []
  ans_u = []
  for i in range(1,lim+1):
    if (N % i): continue
    ans_l.append(i)
    j = N // i
    if j != i:
      ans_u.append(j)
  return ans_l + ans_u[::-1]

# 拡張ユークリッド互除法
# a*x + b*y = gcd(a,b)なるx,yを返し、最後にgcd(a,b)>0を返す
# mod が素数でない時の逆元はこちらを使って求める
def ext_gcd(a, b):
  flag = False
  if abs(b) > abs(a): 
    a, b = b, a
    flag = True
  if b == 0:
    if flag: 
      if a < 0: return 0, -1, -a
      else: return 0, 1, a
    if a < 0: return -1, 0, -a
    return 1, 0, a
  xp, yp, d = ext_gcd(b, a % b)
  x = yp
  y = xp - (a//b) * yp
  if flag:
    x, y = y, x
  return x, y, d

# 中国人剰余定理
# x = R[i] (mod M[i])なるxが存在すれば(x, lcm(M)), 存在しなければ(0,0)を返す
# ext_gcdを併記すること！！
def chinese_remainder_theorem(R, M):
  if len(R) == 0 or len(R) != len(M): return 0, 1 # 要素がないなら(0,1)を返す
  
  N = len(R)
  r0 = R[0]
  m0 = M[0]
  
  for i in range(N):
    r1 = R[i] % M[i]; m1 = M[i];
     
    x, y, d = ext_gcd(m0, m1) # x*m0 + y*m1 = d = gcd(m0, m1)
    if r0 % d != r1 % d: return 0, 0 
    
    s = (r1 - r0) // d # s*x*m0 + s*y*m1 = r1 - r0
    ans = r0 + s*x*m0 # = r1 - s*y*m1 だからこれが答え
    
    # 次の条件のための更新
    m0 = m0*m1//d
    r0 = ans % m0
    
  return r0, m0

# floor_sum
# math.floor((a * i + b) / m) の 0 <= i <= N-1 の和を計算
import sys
sys.setrecursionlimit(10**6)
def floor_sum(n, m, a, b): 
  if n == 0: return 0
  ans = 0
  ans += (n * (n-1) // 2) * (a // m)
  ans += n * (b // m)
  a %= m
  b %= m
  y = (a * (n-1) + b) // m
  ans += y
  return ans + floor_sum(y, a, m, (a * (n-1) + b) % m)

# V以下の数に限り、素因数分解する O(VlogV + QlogV) V:入力上限, Q:factoringの呼び出し回数
V = 2 * 10 ** 6 + 1 
jump_to = [-1] * (V + 1)
for p in range(2, V + 1):
  if jump_to[p] != -1: continue
  jump_to[p] = 1
  for q in range(p * p, V + 1, p):
    jump_to[q] = q // p
def factoring_with_preprocess(n):
  fac = []
  while n > 1:
    fac.append(n // jump_to[n])
    n = jump_to[n]
  return fac # 例: 60 -> [2, 2, 3, 5]

# 前処理なしの素因数分解 １回あたりO(V^(1/2))　V:入力
import math
def factoring(n):
  fac = []
  M = math.ceil(math.sqrt(n)) + 2
  vis = [False] * M
  for p in range(2, M):
    if vis[p]: continue
    if p * p > n: break
    while n % p == 0:
      n //= p
      fac.append(p)
    for q in range(p, M, p):
      vis[q] = True
  if n > 1:
    fac.append(n)
  return fac

from math import sqrt, ceil
def Wheel_Sieve(N): # N以下の素数の列挙
  # N以下の素因数を列挙
  if N <= 1:
    return []
  elif N <= 5:
    return [p for p in range(2, N+1) if p != 4]
  
  ans = []
  M = ceil(sqrt(N) + 1)
  # Step1: w = p1 * p2 * ... * pr <= M　なる、要素が最小の素数列{pi}を求める
  vis = [False] * (M+1)
  w = 1
  for p in range(2, M+1):
    if vis[p]: continue
    w *= p 
    if w * p > M: break
    ans.append(p)
    for q in range(p, M+1, p):
      vis[q] = True
    
  
  # Step2: w = p1 * p2 * ... * prと互いに素な、w以下の数の集合Sを求める 
  S = [v for v in range(1, w+1) if not vis[v]]
  
  # Step3: Sの中から、小さい順に素数を見つける
  ans2 = [] 
  min_prime_factor = [0] * ((N+1)//2) # これのせいで線形。辞書を使うとオーダー改善するが定数倍が重い
  for s1 in range(0, N+1, w):
    for s0 in S:
      s = s1 + s0
      if s == 1: continue
      if s > N: break
      if min_prime_factor[s//2] == 0:
        ans2.append(s)
        mpf = s
      else:
        mpf = min_prime_factor[s//2]
      for p in ans2:
        if p > mpf: break
        if p * s > N: break
        min_prime_factor[p * s // 2] = p
      
  return ans + ans2
