import math
def intersection(C1, C2): #2円C1, C2の交点
  x1, y1, r1 = C1
  x2, y2, r2 = C2
  xr = x2 - x1; yr = y2 - y1;
  if abs(-r2**2 + (r1**2 + xr**2 + yr**2)) < abs(-r1**2 + (r2**2 + xr**2 + yr**2)):
    x1, y1, r1, x2, y2, r2 = x2, y2, r2, x1, y1, r1
    xr *= -1
    yr *= -1
  R2 = xr**2 + yr**2
  R = math.sqrt(R2)
  aux = -r2**2 + (r1**2 + R2)
  s = r1+r2+R
  D = s*(s-2*r1)*(s-2*r2)*(s-2*R)
  if D < 0.: 
    return []
  D = max(0., D)
  xm = (xr * aux) / (2*R2) + x1
  ym = (yr * aux) / (2*R2) + y1
  dx = (yr * math.sqrt(D)) / (2*R2)
  dy = -(xr * math.sqrt(D)) / (2*R2)
  return (xm + dx, ym + dy), (xm - dx, ym - dy)
