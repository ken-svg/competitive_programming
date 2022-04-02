# 角度付きの点 arg: 偏角(double),  
# 偏角ソート時の大小比較に使用する。
# クラスの生成と扱いにより、点の数が2*10**5程度であれば間に合う。10**6程度となると間に合わない(PyPy)。
# 間に合う：　https://atcoder.jp/contests/abc225/submissions/26978638
# 間に合わない：　https://atcoder.jp/contests/typical90/submissions/26978564

import math
atan2 = math.atan2
pi = math.pi

class point_with_arg(): # 1点を表すクラス
  def __init__(self, x, y, c = 0): # c:何周目か
    self.x = x
    self.y = y
    self.arg = atan2(y, x) + c * 2 * pi
  
  """
  誤解を招くのでコメントアウトします
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y and self.arg - other.arg < 1
  """
  
  def __lt__(self, other):
    da = self.arg - other.arg
    return da < 0 if (da > 0.1 or da < -0.1) else self.x * other.y > other.x * self.y
  
  def __le__(self, other):
    da = self.arg - other.arg
    return da <= 0 if (da > 0.1 or da < -0.1) else self.x * other.y >= other.x * self.y
    
  def get(self): # 点の情報を出力
    return (self.x, self.y, self.arg)
  
