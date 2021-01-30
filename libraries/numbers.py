# 逆元
mod = 10**9 + 7
# mod = 
_inv_t = {}
_inv_t[1] = 1
_inv_t[0] = 0
def inv(x):
  if x not in _inv_t:
    _inv_t[x] = inv(mod % x) * (mod - mod // x) % mod
  return _inv_t[x]

# floor_sum
import sys
sys.setrecursionlimit(10**6)
def floor_sum(n, m, a, b): # math.floor((a * i + b) / m) の 0 <= i <= N-1 の和を計算
  if n == 0: return 0
  ans = 0
  ans += (n * (n-1) // 2) * (a // m)
  ans += n * (b // m)
  a %= m
  b %= m
  y = (a * (n-1) + b) // m
  ans += y
  return ans + floor_sum(y, a, m, (a * (n-1) + b) % m)
