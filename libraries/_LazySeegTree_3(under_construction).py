# LazySegmentTree
import pypyjit
pypyjit.set_param('max_unroll_recursion=-1')
N = int(input())
# 頂点数 (N)
V = 1 << ((N - 1).bit_length())

# モノイド演算
ie = [0, 0]
def op(x, y):
  return [x[0] + y[0], x[1] + y[1]]
# 作用
ic = -1
def act(x, a):
  if a == ic:
    return x
  return [a * x[1], x[1]]
# 作用の合成
def cp(a, b):
  if b == ic:
    return a
  return b

data = [ie for _ in range(2 * V)]
lazy = [ic for _ in range(2 * V)]
def _upd(p, l, r):
  lazy_p = lazy[p]
  data[p] = act(data[p], lazy_p)
  lazy[p] = ic
  if p < V:
    a = p; b = p + 1;
    lazy[(p << 1)] = cp(lazy[(p << 1)], lazy_p)
    lazy[(p << 1) | 1] = cp(lazy[(p << 1) | 1], lazy_p)
    d = (l.bit_length() - p.bit_length())
    a <<= d; b <<= d;
    if a < l or r < b:
      c = (a + b) // 2
      if l < c:
        _upd((p << 1), l, r)
      if c < r:
        _upd((p << 1) | 1, l, r)
      data[p] = op(act(data[(p << 1)], lazy[(p << 1)]), act(data[(p << 1) | 1], lazy[(p << 1) | 1]))
        
def _value(p, l, r):
  a = p; b = p + 1;
  d = (l.bit_length() - p.bit_length())
  a <<= d; b <<= d;
  if l <= a and b <= r:
    return data[p]
  else:
    c = (a + b) // 2
    val = ie
    if l < c:
      val = op(val, _value((p << 1), l, r))
    if c < r:
      val = op(val, _value((p << 1) | 1, l, r))
    data[p] = op(act(data[(p << 1)], lazy[(p << 1)]), act(data[(p << 1) | 1], lazy[(p << 1) | 1]))
    return val
    
def _action(p, l, r, v):
  a = p; b = p + 1;
  d = (l.bit_length() - p.bit_length())
  a <<= d; b <<= d;
  if l <= a and b <= r:
    lazy[p] = cp(lazy[p], v)
  else:
    c = (a + b) // 2
    if l < c:
      _action((p << 1), l, r, v)
    if c < r:
      _action((p << 1) | 1, l, r, v)
  
def lst_apply(l, r):
  l |= V; r += V;
  _upd(1, l, r)
  return _value(1, l, r)

def lst_action(l, r, v):
  l |= V; r += V;
  _upd(1, l, r)
  _action(1, l, r, v)
  
def lst_construct(A):
  for i in range(V):
    if i < len(A):
      data[V | i] = A[i]
  for p in range(V-1, 0, -1):
    data[p] = op(data[(p << 1)], data[(p << 1) | 1])
