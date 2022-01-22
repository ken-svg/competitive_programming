# 順序つき集合。
# とても遅い
class ordered_set():
  # 同じ数を挿入した場合、重複はカウントされない
  
  def __init__(self):
    self.unordered_set = set()
    self.inf = 1 << 62
    self.root = [self.inf, None, None, 0] 
    # nodeは[値, 左の子, 右の子, 高さ] で表す
    
  def find(self, x):
    return x in self.unordered_set
  
  def left_max(self, x): # x以下の最大のもの
    if x in self.unordered_set: return x
    p = self.root
    l = -self.inf
    r = self.inf
    while True:
      v = p[0]
      if x < v: # 左に下る
        p = p[1]
        r = v
      else: # 右に下る
        p = p[2]
        l = v
      if p is None:
        return l if l > -self.inf else None
        
  def right_min(self, x): # x以上の最小のもの
    if x in self.unordered_set: return x
    p = self.root
    l = -self.inf
    r = self.inf
    while True:
      v = p[0]
      if x < v: # 左に下る
        p = p[1]
        r = v
      else: # 右に下る
        p = p[2]
        l = v
      if p is None:
        return r if r < self.inf else None  
  
  def _right_rotate(self, p, pp, direction): # 左が重いとき
    # p : 回転で降下する頂点、pp: pの親頂点 
    # direction: pがppのどちら向きの子か(左ならTrue, 右ならFalse)
    
    q = p[1]
    r = q[2]
    
    # ppの更新
    if direction: # pがppの左子のとき
      pp[1] = q # 左子の更新
    else:
      pp[2] = q # 右子の更新
    pplh = 0 if pp[1] is None else pp[1][3] + 1
    pprh = 0 if pp[2] is None else pp[2][3] + 1
    pp[3] = max(pplh, pprh)
      
    # pの更新
    p[1] = r
    plh = 0 if r is None else r[3] + 1
    prh = 0 if p[2] is None else p[2][3] + 1 
    p[3] = max(plh, prh)
    
    # qの更新
    q[2] = p
    qlh = 0 if q[1] is None else q[1][3] + 1
    qrh = 0 if p is None else p[3] + 1 
    q[3] = max(qlh, qrh)
    
  def _left_rotate(self, p, pp, direction): # 右が重いとき
    # p : 回転で降下する頂点、pp: pの親頂点 
    # direction: pがppのどちら向きの子か(左ならTrue, 右ならFalse)
    
    q = p[2]
    r = q[1]
    
    # ppの更新
    if direction: # pがppの左子のとき
      pp[1] = q # 左子の更新
    else:
      pp[2] = q # 右子の更新
    pplh = 0 if pp[1] is None else pp[1][3] + 1
    pprh = 0 if pp[2] is None else pp[2][3] + 1
    pp[3] = max(pplh, pprh)
      
    # pの更新
    p[2] = r
    plh = 0 if p[1] is None else p[1][3] + 1
    prh = 0 if p[2] is None else p[2][3] + 1 
    p[3] = max(plh, prh)
    
    # qの更新
    q[1] = p
    qlh = 0 if q[1] is None else q[1][3] + 1
    qrh = 0 if q[2] is None else q[2][3] + 1 
    q[3] = max(qlh, qrh)    
    
  def add(self, x):
    p = self.root
    
    # 探索
    path = [p]
    directions = []
    while True:
      v = p[0]
      if v == x: return # 値が重複するので更新しない
      elif x < v: # 左に下る
        if p[1] is None:
          p[1] = [x, None, None, 0]
          break
        p = p[1]
        path.append(p)
        directions.append(True)
      else: # 右に下る
        if p[2] is None:
          p[2] = [x, None, None, 0]
          break
        p = p[2]
        path.append(p)
        directions.append(False)
    
    self.unordered_set.add(x)
    
    # 中間結果
    # p: 新たに追加した頂点の親
    # path: rootからpまでの道
    # directions: 道の途中で進んだ方向の記録
    
    # 平衡
    for i in range(len(directions)-1, -1, -1):
      p = path[i+1]
      
      plh = 0 if p[1] is None else p[1][3] + 1
      prh = 0 if p[2] is None else p[2][3] + 1
      
      if prh == plh + 2:
        q = p[2]
        qlh = 0 if q[1] is None else q[1][3] + 1
        qrh = 0 if q[2] is None else q[2][3] + 1
        if qlh > qrh: # 下の頂点の左側が重たい場合(right-left case)
          self._right_rotate(q, p, directions[i+1])  
        pp = path[i]
        self._left_rotate(p, pp, directions[i])
        break # 挿入の場合は、もとと高さが変わらないはずなので終了
        
      elif plh == prh + 2:
        q = p[1]
        qlh = 0 if q[1] is None else q[1][3] + 1
        qrh = 0 if q[2] is None else q[2][3] + 1
        if qrh > qlh: # 下の頂点の左側が重たい場合(left-right case)
          self._left_rotate(q, p, directions[i+1])  
        pp = path[i]
        self._right_rotate(p, pp, directions[i])
        break
        
      elif prh == plh: # 高さが変わらないなら終了
        break
      

# Sorted setを平方分割と立方分割で実装。後者は遅くて使い物にならない。
# https://atcoder.jp/contests/abc217/submissions/28667455
import math
from bisect import bisect_left, bisect_right
REBUILD_RATIO_UPPER = 100
REBUILD_RATIO_LOWER = 0.00001
class SortedSet_1():
  def __init__(self, A):
    self.REBUILD_RATIO_UPPER = 10
    self.REBUILD_RATIO_LOWER = 0.00001
    self.BACKET_RATIO = 3
    self.n = len(A)
    self.sqrt_n = math.floor(math.sqrt(self.n)+10**(-10))
    self.A = A
    self.construct()
    
  def __len__(self):
    A = self.A
    if isinstance(A[0], list):
      return sum([len(a) for a in A])
    else:
      return len(A)
    
  def __iter__(self):
    for A1 in self.A:
      for a in A1:
        yield a
    
  def __min__(self):
    return self.A[0][0]
  
  def __max__(self):
    return self.A[-1][-1]
  
  #def __print__(self):
  #  print(self.A)
    
  def construct(self):
    A = self.A
    n = self.n
    sqrt_n = self.sqrt_n
    
    if isinstance(A[0], list):
      A_new = []
      for a in A:
        A_new.extend(a)
      A = A_new
      
    A_new = []
    tmp = []
    backet_number = max(1, sqrt_n // self.BACKET_RATIO)
    self.A = A = [A[v//backet_number : (v + n)//backet_number] for v in range(0, n * backet_number, n)]
    #print(self.A)
    self.A_top = [A1[0] for A1 in A] 
    self.A_bottom = [A1[-1] for A1 in A] 
 
  def add(self, x):
    A = self.A
    A_top = self.A_top
    A_bottom = self.A_bottom
    
    # insert
    i1 = max(0, bisect_right(A_top, x) - 1)
    A1 = A[i1]
    A1.insert(bisect_left(A1, x), x)
    
    self.n += 1
    if pow(self.sqrt_n + 1, 2) == self.n:
      self.sqrt_n += 1
 
    # check valance condition
    if len(A1) >= (self.sqrt_n * self.REBUILD_RATIO_UPPER): 
      # if the valance condition is not satisfied, reconstruct A 
      self.construct()
      return
 
    # update A_top and A_bottom
    A_top[i1] = A1[0]
    A_bottom[i1] = A1[-1]
 
  def remove(self, x, remove_all=False):
    A = self.A
    A_top = self.A_top
    A_bottom = self.A_bottom
    
    # delete
    i1 = bisect_right(A_top, x) - 1
    if i1 == -1: return False
    A1 = A[i1]
    i2 = bisect_left(A1, x)
    if i2 == len(A1) or A1[i2] != x: return False
    A1.pop(i2)
 
    self.n -= 1
    if pow(self.sqrt_n, 2) > self.n:
      self.sqrt_n -= 1  
 
    # check valance condition
    if len(A1) <= (self.sqrt_n * self.REBUILD_RATIO_LOWER): 
      # if the valance condition is not satisfied, reconstruct A 
      self.construct()
      return True
 
    # update A_top and A_bottom
    A_top[i1] = A1[0]
    A_bottom[i1] = A1[-1]
    return True
 
 
  def gt(self, x):
    A = self.A
    i1 = bisect_right(self.A_bottom, x)
    if i1 == -1: return None # No element is greater than x
    A1 = A[i1]
    return A1[bisect_right(A1, x)]
 
  def ge(self, x):
    A = self.A
    A_bottom = self.A_bottom
    i1 = bisect_left(self.A_bottom, x)
    if i1 == len(A_bottom): return None # No element is greater than x or equal to x
    A1 = A[i1]
    return A1[bisect_left(A1, x)]
 
  def lt(self, x):
    A = self.A
    i1 = bisect_left(self.A_top, x) - 1
    if i1 == -1: return None # No element is less than x
    A1 = A[i1]
    return A1[bisect_left(A1, x) - 1]
 
  def le(self, x):
    A = self.A
    A_top = self.A_top
    i1 = bisect_right(A_top, x) - 1
    if i1 == len(A_top): return None # No element is less than x or equal to x
    A1 = A[i1]
    return A1[bisect_right(A1, x) - 1]
 
class SortedSet_2():
  def __init__(self, A):
    self.n = len(A)
    self.cbrt_n = math.floor(pow(self.n, 1./3.)+10**(-10))
    self.A = [A]
    self.construct()
    
  def __len__(self):
    A = self.A
    return sum([len(a) for a in A])
  
  def __iter__(self):
    for A1 in self.A:
      for a in A1:
        yield a
    
  def __min__(self):
    return min(self.A[0])
  
  def __max__(self):
    return max(self.A[-1])
  
  #def __print__(self):
  #  print([A1 for A1 in A])
    
  def construct(self):
    A = self.A
    A_new = []
    for A1 in A:
      for a in A1:
        A_new.append(a)
    A = A_new
 
    n = self.n
    cbrt_n = self.cbrt_n
    A_new = []
    self.A = A = [SortedSet_1(A[v//cbrt_n : (v + n)//cbrt_n]) for v in range(0, n * cbrt_n, n)]
    self.A_top = [min(A1) for A1 in A] 
    self.A_bottom = [max(A1) for A1 in A] 
 
  def add(self, x):
    A = self.A
    A_top = self.A_top
    A_bottom = self.A_bottom
    
    # insert
    i1 = max(0, bisect_right(A_top, x) - 1)
    A1 = A[i1]
    A1.add(x)
    
    self.n += 1
    if pow(self.cbrt_n + 1, 3) == self.n:
      self.cbrt_n += 1
 
    # check valance condition
    if len(A1) >= (self.cbrt_n **2 * REBUILD_RATIO_UPPER): 
      # if the valance condition is not satisfied, reconstruct A 
      self.construct()
      return
 
    # update A_top and A_bottom
    A_top[i1] = min(A1)
    A_bottom[i1] = max(A1)
 
  def remove(self, x, remove_all=False):
    A = self.A
    A_top = self.A_top
    A_bottom = self.A_bottom
    
    # delete
    i1 = bisect_right(A_top, x) - 1
    if i1 == -1: return False
    A1 = A[i1]
    flag = A1.remove(x)
    if not flag: return False
 
    self.n -= 1
    if pow(self.cbrt_n, 3) > self.n:
      self.cbrt_n -= 1  
 
    # check valance condition
    if len(A1) <= (self.cbrt_n **2 * REBUILD_RATIO_LOWER): 
      # if the valance condition is not satisfied, reconstruct A 
      self.construct()
      return True
 
    # update A_top and A_bottom
    A_top[i1] = min(A1)
    A_bottom[i1] = max(A1)
    return True
 
 
  def gt(self, x):
    A = self.A
    A_bottom = self.A_bottom
    i1 = bisect_right(A_bottom, x)
    if i1 == len(A_bottom): return None # No element is greater than x
    A1 = A[i1]
    return A1.gt(x)
 
  def ge(self, x):
    A = self.A
    A_bottom = self.A_bottom
    i1 = bisect_left(A_bottom, x)
    if i1 == len(A_bottom): return None # No element is greater than x or equal to x
    A1 = A[i1]
    return A1.ge(x)
 
  def lt(self, x):
    A = self.A
    A_top = self.A_top
    i1 = bisect_left(A_top, x) - 1
    if i1 == -1: return None # No element is less than x
    A1 = A[i1]
    return A1.lt(x)
 
  def le(self, x):
    A = self.A
    A_top = self.A_top
    i1 = bisect_right(A_top, x) - 1
    if i1 == len(A_top): return None # No element is less than x or equal to x
    A1 = A[i1]
    return A1.le(x)
