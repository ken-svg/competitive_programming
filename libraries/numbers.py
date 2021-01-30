# 逆元
mod = 10**9 + 7
# mod = 素数
_inv_t = {}
_inv_t[1] = 1
_inv_t[0] = 0
def inv(x):
  if x not in _inv_t:
    _inv_t[x] = inv(mod % x) * (mod - mod // x) % mod
  return _inv_t[x]

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
