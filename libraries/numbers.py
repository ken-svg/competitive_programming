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
