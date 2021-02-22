# suffix arrray
# O(n(logn)^2)

def sa_log(S):
  global it
  if isinstance(S, str):
    S = [ord(s) for s in S]
  S_max = max(S)
  S_min = min(S)
  S = [s - S_min + 1 for s in S]
  K = S_max - S_min + 1 + 1
  S.append(0)
  
  N = len(S)
  
  pre_ans = S
  
  def conv(a, b, c):
    return (a * (2*N+1) + b) * N + c
  def inv(info):
    info2 = info // N
    a = info2 // (2*N+1)
    b = info2 % (2*N+1)
    c = info % N
    return a, b, c
  
  interval = 0
  while interval < N:
    to_be_sorted = []
    for i in range(N-interval):
      to_be_sorted.append(conv(pre_ans[i], pre_ans[i+interval], i))
    for i in range(N-interval, N):
      to_be_sorted.append(conv(pre_ans[i], 0, i))
    to_be_sorted.sort()
    del pre_ans
    pre_ans = [-1]*N
    idx = -1
    p1, p2 = -2, -2
    for info in to_be_sorted:
      k1, k2, i = inv(info)
      if not(p1 == k1 and p2 == k2):
        idx += 1
        p1, p2 = k1, k2
      pre_ans[i] = idx
    if interval == 0: interval = 1
    else: interval <<= 1
  return [inv(info)[2] for info in to_be_sorted]
