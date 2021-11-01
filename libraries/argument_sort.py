# 角度付きの点 arg: 偏角(double),  
# 偏角ソート時の大小比較に使用する。

import math
atan2 = math.atan2
pi = math.pi
class point_with_arg():
  def __init__(self, x, y, c = 0): # c: 何周目か
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
    if da > 0.1:
      return False
    elif da < -0.1:
      return True
    else:
      return self.x * other.y < other.x * self.y
  
  def __le__(self, other):
    da = self.arg - other.arg
    if da > 0.1:
      return False
    elif da < -0.1:
      return True
    else:
      return self.x * other.y <= other.x * self.y
  
  def __gt__(self, other):
    da = self.arg - other.arg
    if da > 0.1:
      return True
    elif da < -0.1:
      return False
    else:
      return self.x * other.y > other.x * self.y
  
  def __ge__(self, other):
    da = self.arg - other.arg
    if da > 0.1:
      return True
    elif da < -0.1:
      return False
    else:
      return self.x * other.y >= other.x * self.y
  
"""  
N = int(input())

points = [list(map(int,input().split())) for _ in range(N)]

from math import atan2
from math import pi
def main(i, p):
  x, y = p
  
  infos = [point_with_arg(1, 0, c = 6)]
  for j in range(N):
    if j == i: continue
    q = points[j]
    x1, y1 = q
    
    dx = x1 - x
    dy = y1 - y
    #arg = atan2(dy, dx)
    
    infos.append(point_with_arg(dx, dy, c = 0))
    infos.append(point_with_arg(dx, dy, c = 1))
    
  infos.sort()
  
  tmp_ans = 0
  idx = 0
  for jdx in range(N-1):
    while infos[idx].arg < infos[jdx].arg + pi:
      idx += 1
    #print(infos[idx], infos[idx-1], infos[jdx])  
    tmp_ans = max(tmp_ans, 2 * pi - (infos[idx].arg - infos[jdx].arg), (infos[idx-1].arg - infos[jdx].arg))
    
  return tmp_ans
    
    
      
ans = -1
for i, p in enumerate(points):
  ans = max(ans, main(i, p))
  
print(ans * 180 / pi)
"""  


