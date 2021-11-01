# 分数
# いまのところ、大小比較のみ

import math
class fraction:
  def __init__(self, numer, denom):
    d = math.gcd(numer, denom)
    numer //= d
    denom //= d
    if denom < 0:
      denom *= -1
      numer *= -1
    self.numer = numer
    self.denom = denom
  
  def __lt__(self, other):
    return self.numer * other.denom < other.numer * self.denom
  
  def __le__(self, other):
    return self.numer * other.denom <= other.numer * self.denom
  
  def __gt__(self, other):
    return self.numer * other.denom > other.numer * self.denom
  
  def __ge__(self, other):
    return self.numer * other.denom >= other.numer * self.denom
  
  def __eq__(self, other):
    return self.numer * other.denom == other.numer * self.denom
