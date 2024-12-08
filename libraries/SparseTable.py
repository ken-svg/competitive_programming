class Sparse_Table(): # 静的なrange query(半群を与える演算について)
  def __init__(self, A, op = min):
    self.A = A
    self.op = op
    self.N = N = 1 << (len(A).bit_length())
    V = A + [0] * (N - len(A)) # 演算可能な値を適当に。（単位元がある場合は単位元を入れた方が良い）
    step = 4
    while step <= N:
      half = step >> 1
      D = V[:N]
      for section in range(0, len(A), step):
        section_half = section | half
        for i in range(section_half - 2, section - 1, -1):
          D[i] = op(D[i], D[i+1])
        for i in range(section_half + 1, section + step):
          D[i] = op(D[i-1], D[i])
      for v in D:
        V.append(v)
      step <<= 1
    self.V = V
    
  def apply(self, l, r): # apply self.op on [l, r) (0-indexed)
    r -= 1
    if l > r: return None
    elif l == r: return self.A[l]
    c = (l ^ r).bit_length() - 1
    return self.op(self.V[(c * self.N) | l], self.V[(c * self.N) | r])
