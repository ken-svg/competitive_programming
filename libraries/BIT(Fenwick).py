#BIT(Fenwick Tree)

class BIT: 
  """ n: 要素数, op: 演算（可逆かつ可換）, ie: 単位元, inv: 逆元 """
  """ 逆元を持つ、可換な演算に対して適用可能 """
  def __init__(self, n, op=lambda x,y: x+y, inv=lambda x:-x, ie = 0): # 要素数のみ指定すれば使用可能。演算opを指定しない場合は通常加算となる。
    self.n = n
    self.op = op
    self.ie = ie
    self.inv = inv
    self.el = [ie]*(n+1) 
    self.data = [ie]*(n+1)
  
  def add(self, i, x):
    op = self.op
    self.el[i] = op(self.el[i], x)
    data = self.data
    while i <= self.n:
      data[i] = op(data[i], x)
      i += i & -i
      
  def _obtain(self, i): # sum from 1 to i
    data = self.data
    op = self.op
    ans = 0
    while i > 0:
      ans = op(data[i], ans)
      i -= i & -i
    return ans
    
  def apply(self, l, r):
    return  self.op(self.inv(self._obtain(l-1)), self._obtain(r-1))
      
  def construct(self, A):
    for i, x in enumerate(A):
      self.add(i+1,x)     
      
    
# 利点：
# 区間総和をO(log N)の時間で行うことができる。
# 上記のメリットを享受しながら、1点の更新時間をO(log N)に抑えられる

# 注意点（主にセグメントツリーとの差別化）：
# ・逆元が必要
# ・この実装例では、演算が可換であることを要請している
# ・更新演算addがupdate(上書き)ではないので注意を要する
# ・1-index(重要)

# 用法一覧：
# def construct(self, A): # 初期値配列Aをインプットし、BITを構築する
# def add(self, i, x): # i番目にxを加算
# def apply(self, l, r): # 半開区間[l, r)の総和を計算
# self.el[i]: # i番目の要素の現在の値

    
  
