# example:
# https://atcoder.jp/contests/abc324/submissions/46641103

class BitVector(): # Rank and select
  def __init__(self, A):
    self.len_A = len(A)
    self.R1 = R1 = [0]
    self.S0 = S0 = []
    self.S1 = S1 = []
    for i, a in enumerate(A):
      if a == 0:
        S0.append(i)
        R1.append(R1[-1])
      else:
        S1.append(i)
        R1.append(R1[-1] + 1)
        
  def rank(self, target, pos): # number of target in A[0:pos] (include pos)
    if target:
      return self.R1[pos+1]
    else:
      return pos + 1 - self.R1[pos+1]
      
  def select(self, target, num): # position of num'th target(0 or 1)
    if target:
      if num > len(self.S1):
        return None
      return self.S1[num-1]
    else:
      if num > len(self.S0):
        return None
      return self.S0[num-1]
      
from collections import defaultdict as dft      
class WaveletMatrix(): # メモリ量には気を遣っていない
  def __init__(self, A):
    self.len_A = len(A)
    self.A0 = [a for a in A]
    self.sigma = max(A).bit_length()
    self.BV = BV = []
    self.TH = TH = []
    for b in range(self.sigma-1, -1, -1):
      B_now = [(a >> b) & 1 for a in A]
      A_next_0 = []
      A_next_1 = []
      for a, b in zip(A, B_now):
        if b:
          A_next_1.append(a)
        else:
          A_next_0.append(a)
          
      BV.append(BitVector(B_now))
      TH.append(len(A_next_0))
      
      A = A_next_0 + A_next_1
      
    self.A_sorted = [a for a in A]
    self.A_sorted_pos = A_sorted_pos = dft(int)
    for i, a in enumerate(A):
      if a in A_sorted_pos: continue
      A_sorted_pos[a] = i
    
  def __getitem__(self, i):
    return self.A0[i]
    
  def rank(self, target, pos): # number of target in A[0:pos] (include pos)
    if target not in self.A_sorted_pos or pos == -1: return 0
    i = 0
    BV = self.BV
    TH = self.TH
    for b in range(self.sigma-1, -1, -1):
      t = (target >> b) & 1
      pos = TH[i] * t + BV[i].rank(t, pos) - 1
      i += 1
    return pos - self.A_sorted_pos[target] + 1
    
  def select(self, target, num): # position of num'th target
    if num == 0 or target not in self.A_sorted_pos:
      return -1
    pos = self.A_sorted_pos[target] + num - 1
    BV = self.BV
    TH = self.TH
    i = -1
    for b in range(self.sigma):
      if pos is None or pos >= self.len_A: return -1
      t = (target >> b) & 1
      pos = BV[i].select(t, pos - TH[i] * t + 1)
      i -= 1
    if pos is None or pos >= self.len_A or self.A0[pos] != target: return -1
    return pos
    
  def quantile(self, s, e, k): # find k'th least number in A[s:e] (include e)
    if not(0 < k <= e - s + 1): return None
    pos_l = s-1
    pos_r = e

    BV = self.BV
    TH = self.TH
    k -= 1
    i = 0
    for b in range(self.sigma-1, -1, -1):
      c0 = BV[i].rank(0, pos_r) - BV[i].rank(0, pos_l)
      if k >= c0:
        k -= c0
        t = 1
      else:
        t = 0
      pos_l = TH[i] * t + BV[i].rank(t, pos_l) - 1
      pos_r = TH[i] * t + BV[i].rank(t, pos_r) - 1
      i += 1
    return self.A_sorted[pos_l + k + 1]
  
  def lowerfreq(self, s, e, y): # count numbers "< y" in A[s:e] (include e)
    if y <= 0 or s > e: 
      return 0
    if y >= 1 << self.sigma: return e - s + 1 
    pos_l = s-1
    pos_r = e
    i = 0
    BV = self.BV
    TH = self.TH
    ans = 0
    for b in range(self.sigma-1, -1, -1):
      t = (y >> b) & 1
      if t:
        ans += BV[i].rank(0, pos_r) - BV[i].rank(0, pos_l)
      pos_l = TH[i] * t + BV[i].rank(t, pos_l) - 1
      pos_r = TH[i] * t + BV[i].rank(t, pos_r) - 1
      i += 1
    return ans
    
  def rangefreq(self, s, e, x, y): # count numbers "< y" and ">= x" in A[s:e] (include e)
    if x >= y: return 0
    return self.lowerfreq(s, e, y) - self.lowerfreq(s, e, x)
