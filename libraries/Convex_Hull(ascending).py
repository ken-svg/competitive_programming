from math import gcd
from bisect import bisect
class fraction():
  def __init__(self, num, den): # num / den
    if den < 0:
      num *= -1
      den *= -1
    d = gcd(num, den)
    self.num = num // d
    self.den = den // d
  def __add__(self, other):
    num = self.den * other.num + self.num * other.den
    den = self.den * other.den 
    return fraction(num, den)
  def __sub__(self, other):
    num = self.den * other.num - self.num * other.den
    den = self.den * other.den 
    return fraction(num, den)
  def __mul__(self, other):
    num = self.num * other.num
    den = self.den * other.den 
    return fraction(num, den)
  def __truediv__(self, other):
    num = self.num * other.den
    den = self.den * other.num
    return fraction(num, den)
  def __eq__(self, other):
    return self.num == other.num and self.den == other.den
  def __nq__(self, other):
    return self.num != other.num or self.den != other.den
  def __lt__(self, other):
    return self.num * other.den < other.num * self.den
  def __gt__(self, other):
    return self.num * other.den > other.num * self.den
  def __le__(self, other):
    return self.num * other.den <= other.num * self.den
  def __ge__(self, other):
    return self.num * other.den >= other.num * self.den
  def __str__(self):
    return "{}/{}".format(self.num, self.den) if self.den > 1 else str(self.num)
  def __float__(self):
    return self.num / self.den
  def __int__(self):
    return self.num // self.den
  

from math import gcd
class convex_hull(): # 直線群の最大値からなる下に凸な曲線を管理 傾きは短調増加
  def __init__(self):
    self.info = []
    self.A = []
    self.B = []
    self.intersection = []
    
  def append(self, a, b): # 直線 y = a*x + b の追加(aは単調増加)
    A = self.A
    B = self.B
    intersection = self.intersection
    if isinstance(a, int):
      a = fraction(a, 1)
    if isinstance(b, int):
      b = fraction(b, 1)
    while intersection:
      ap, bp = A[-1], B[-1]
      x = intersection[-1]
      if ap * x + bp > a * x + b: break
      A.pop()
      B.pop()
      intersection.pop()
    if A:
      ap, bp = A[-1], B[-1]
      x = (b - bp) / (ap - a)
      intersection.append(x)
    A.append(a)
    B.append(b)  
  
  def value(self, x): # 点xでの値を求める
    if isinstance(x, int):
      x = fraction(x, 1)
    idx = bisect(self.intersection, x)
    return self.A[idx] * x + self.B[idx]
  
  def __str__(self):
    ans = ["<convex_hull> \n lines: "]
    for a, b in zip(self.A, self.B):
      ans.append("y = ({}) * x + ({}), ".format(str(a), str(b)))
    ans.append("\n intersections: ")
    for x in self.intersection:
      ans.append("x = {}, ".format(str(x)))
    return "".join(ans)
    
