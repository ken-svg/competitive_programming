import math
def intersection(C1, C2): #2円C1, C2の交点
  x1, y1, r1 = C1
  x2, y2, r2 = C2
  xr = x2 - x1; yr = y2 - y1;
  R2 = xr**2 + yr**2
  R = math.sqrt(R2)
  aux = -(r2**2 - r1**2 - R2)
  D = (2.*R*r1 + aux) * (2.*R*r1 - aux)
  eps = 10.**(-10.)
  if D < -eps*(2.*R*r1)**2: return []
  D = max(0., D)
  xm = (xr * aux) / (2*R2) + x1
  ym = (yr * aux) / (2*R2) + y1
  dx = (yr * math.sqrt(D)) / (2*R2)
  dy = -(xr * math.sqrt(D)) / (2*R2)
  return [(xm + dx, ym + dy), (xm - dx, ym - dy)]
