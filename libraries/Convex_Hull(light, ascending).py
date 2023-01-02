from math import gcd
# 直線の係数が整数または小数の場合
# https://atcoder.jp/contests/jag2015summer-day4/submissions/37699281
def cht_append(a, b, cht_info): # 直線 y = a*x + b の追加(aは単調増加)
  # cht_info = [A分子, B分子, X分母, X分母]
  A_num, B_num, X_num, X_den = cht_info
  a_num = a #; a_den = 1;
  b_num = b #; b_den = 1;
  while X_num:
    ap_num, bp_num = A_num[-1], B_num[-1]
    x_num, x_den = X_num[-1], X_den[-1]
    if (ap_num - a_num) * x_num > (b_num - bp_num) * x_den: break
    A_num.pop()
    B_num.pop()
    X_num.pop()
    X_den.pop()
  if A_num:
    ap_num, bp_num = A_num[-1], B_num[-1]
    if ap_num == a_num:
      if bp_num >= b_num: return
      else: # ストックされた直線が一つしか残っておらず、これから追加する直線がそれと同じ傾きかつ大きい場合のみこのケース
        B_num[-1] = b_num
        return
    x_num, x_den = (b_num - bp_num), (ap_num - a_num)
    d = gcd(x_num, x_den)
    if x_den < 0: d *= -1
    X_num.append(x_num // d)
    X_den.append(x_den // d)
  A_num.append(a_num)
  B_num.append(b_num)  
  
def cht_value(x, cht_info): # 点xでの値を求める(xは整数)
  A_num, B_num, X_num, X_den = cht_info
  if not A_num: return None
  x_num = x
  lt = -1
  rt = len(X_num)
  while rt - lt > 1:
    ct = (rt + lt) // 2
    if x_num * X_den[ct] <= X_num[ct]:
      rt = ct
    else:
      lt = ct
  a_num_rt = A_num[rt]
  b_num_rt = B_num[rt]
  return a_num_rt * x_num + b_num_rt



"""
from math import gcd
class convex_hull():
  def __init__(self):
    self.A = []
    self.B = {}
    self.intersection = []
    self.sect_size = 0
    
  def _fraction(self, x, y):
    d = gcd(abs(x), abs(y))
    if d * y < 0: 
      d *= -1
    #print(x, y, d, x // d, y // d)
    return [x // d, y // d]
  
  def _evaluate_line(self, a, b, f):
    return self._fraction(a * f[0] + b * f[1], f[1])
    
  def _derive_intersection(self, a1, b1, a2, b2):
    if a1 == a2: return False
    else:
      xi = self._fraction(-(b1 - b2), a1 - a2)
      yi = self._evaluate_line(a1, b1, xi)
    return [xi, yi]  
  
  def _fraction_greater(self, y1, y2): # y1 > y2
    return y1[0] * y2[1] > y2[0] * y1[1]
    
  def append(self, a, b): # !!! 追加するaは単調減少 !!!
    A = self.A
    B = self.B
    if len(A) == 0:
      A.append(a)
      B[a] = b
    
    else:
      I = self.intersection
      while I:
        xp, yp = I[-1]
        yn = self._evaluate_line(a, b, xp)
        if self._fraction_greater(yp, yn) or yp == yn: #　直前の交点が不適となる場合
          I.pop()
          ap = A[-1]
          A.pop()
          #B.remove(ap)
        else:
          break
      
      ap = A[-1]
      bp = B[ap]
      if a == ap: return
      
      pi = self._derive_intersection(ap, bp, a, b)
      I.append(pi)
      A.append(a)
      B[a] = b
    
    self.sect_size = len(self.A)
    #print(self.A, self.B, self.intersection)
    return
  
  def derive_min(self, x):
    A = self.A
    B = self.B
    I = self.intersection
    if len(A) == 0:
      return None
    elif len(A) == 1:
      a = A[-1]
      
    else: #elif len(A) == 1:
      if self._fraction_greater([x, 1], I[-1][0]):
        rt = len(I)
        
      else:
        lt = -1
        rt = len(I)
        while rt - lt > 1:
          ct = (rt + lt) // 2
          x0, y0 = I[ct]
          #print(x, lt, rt, ct, x0, self._fraction_greater(x0, [x, 1]))
          if self._fraction_greater(x0, [x, 1]):
            rt = ct
          else:
            lt = ct
      
      a = A[rt]
        
    b = B[a]
    #print("!", a, x, b, a*x+b)
    return a * x + b
"""
