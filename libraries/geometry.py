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


# 偏角ソート(atan2を使わない)
# def argument_sort(vecs), vecs: 二次元ベクトルのリスト, 出力: vecsを偏角ソートしたもの
def _merge_sort(A, is_larger = lambda x, y: x > y): # is_larger(x, y): x > y
  N = len(A)
  tmp_prv = A
  tmp_len = 1
  while tmp_len < N:
    tmp_ans = []
    for start in range(0, N, tmp_len*2):
      kl = start
      kr = start + tmp_len
      kl_max = min(N, kr)
      kr_max = min(max(N, kr), kr + tmp_len)
      while kl < kl_max or kr < kr_max:
        #print(kl, kr, kl_max, kr_max, tmp_prv)
        if kr == kr_max:
          tmp_ans.append(tmp_prv[kl])
          kl += 1
        elif kl == kl_max or is_larger(tmp_prv[kl], tmp_prv[kr]):
          tmp_ans.append(tmp_prv[kr])
          kr += 1
        else:
          tmp_ans.append(tmp_prv[kl])
          kl += 1   
    tmp_len <<= 1 
    tmp_prv = tmp_ans
  return tmp_ans
def is_larger_in_arg(v1, v2): # v1, v2は0でない２次元ベクトル、偏角-180[deg]~180[deg]の大小
  x1, y1 = v1
  x2, y2 = v2
  if y1 == 0 and y2 == 0:
    return x1 > 0 and x2 < 0
  elif y1 == 0:
    if x1 < 0: return False
    else: return y2 < 0 # 第３、４象限
  elif y2 == 0:
    if x2 < 0: return True
    else: return y1 > 0 # 第１、２象限
  else: # x1 != 0 and y1 != 0
    if y1 * y2 < 0: return y1 > 0
    else: # x1 > 0 and x2 > 0 or x1 < 0 and x2 < 0
      return x1 * y2 - x2 * y1 < 0 
  
def argument_sort(vecs):
  return _merge_sort(vecs, is_larger_in_arg)
