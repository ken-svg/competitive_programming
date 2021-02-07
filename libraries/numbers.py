# 逆元
mod = 10**9 + 7
# mod = 素数
_inv_t = {}
_inv_t[1] = 1
_inv_t[0] = 0
def inv(x, mod):
  if x not in _inv_t:
    _inv_t[x] = inv(mod % x, mod) * (mod - mod // x) % mod
  return _inv_t[x]

# 約数列挙 O(\sqrt(N))
import math
def find_divisors(N):
  lim = math.floor(math.sqrt(N)+10**(-10))
  ans_l = []
  ans_u = []
  for i in range(1,lim):
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
