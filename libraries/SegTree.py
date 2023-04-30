#SegTree

class SegTree():
  """ 入出力はすべて0-idx"""
  """ n: 要素数, op: 結合律を満たす演算, ie: 演算opの単位元 """
  def __init__(self, n, op = min, ie = 10**20): # defaultではnのみ入れれば良い。opの指定がない場合、min演算を行う
    self.n = n
    self.size = 1 << (n-1).bit_length()
    self.ie = ie
    self.el = [ie]*n #0-idxの要素
    self.op = op
    self.data = [ie]*(2*self.size) #1以降が有効データ, 桁数で階層を表現
    
  def construct(self, A): # A初期値, 構成
    n = min(self.n,len(A))
    self.el[:n] = A[:n]
    data = self.data; size = self.size; op = self.op;
    data[size:size+n] = A[:n]
    for i in range(size-1,0,-1):
      j = i << 1
      data[i] = op(data[j], data[j+1])

  def update(self, i, x): # i番目をxで更新
    self.el[i] = x
    size = self.size; op = self.op; data = self.data;
    i += size
    data[i] = x
    while i > 1:
      p = data[i>>1]
      v = (op(data[i-1], data[i]) if i & 1 else op(data[i], data[i+1]))
      if p == v: break
      data[i>>1] = v
      i >>= 1

  def apply(self, l, r): # 半開区間[l,r)の計算結果を出力 (0 <= l < r <= N)
    size = self.size; op = self.op; data = self.data;
    r += size; l += size
    ans_lt = ans_rt = self.ie;
    while r - l > 1:
      if l & 1: ans_lt = op(ans_lt, data[l]); l += 1
      if r & 1: ans_rt = op(data[r-1], ans_rt); r -= 1
      r >>= 1; l >>= 1;
    if r - l == 1:
      return op(op(ans_lt, data[l]), ans_rt)
    elif r == l:
      return op(ans_lt, ans_rt)    

      def bisect_left(self, a): 
    # B[i] = st.apply(st[:i]) として、Bを値aについて二分探索。挿入位置（左よせ）を返す。
    # 同じ値があるときは、その値よりも左の位置を返す
    data = self.data
    n = self.n
    if data[1] < a:
      return n
    
    m = len(data) // 2
    
    op = self.op
    
    now_pos = 1
    now_val = self.ie
    while now_pos < m:
      next_pos = (now_pos << 1) | 1
      next_val = op(now_val, data[next_pos - 1])
      if next_val < a:
        now_val = next_val
        now_pos = next_pos
      else:
        now_pos = next_pos - 1
        
    return min(now_pos - m, n-1)
  
  def bisect_right(self, a): 
    # B[i] = st.apply(st[:i]) として、Bを値aについて二分探索。挿入位置（左よせ）を返す。
    # 同じ値があるときは、その値よりも右の位置を返す
    data = self.data
    n = self.n
    if data[1] <= a:
      return n
    
    m = len(data) // 2
    
    op = self.op
    
    now_pos = 1
    now_val = self.ie
    while now_pos < m:
      next_pos = (now_pos << 1) | 1
      next_val = op(now_val, data[next_pos - 1])
      if next_val <= a:
        now_val = next_val
        now_pos = next_pos
      else:
        now_pos = next_pos - 1
        
    return min(now_pos - m, n-1)
  
# 利点：
# 区間総和をO(log N)の時間で行うことができる。
# 上記のメリットを享受しながら、1点の更新時間をO(log N)に抑えられる

# 用法一覧：
# def construct(self, A) # 初期構成。初期値A(配列)をインプットする
# def update(self, i, x) # i番目をxで更新
# def apply(self, l, r) # 半開区間[l,r)の計算結果を出力 (0 <= l < r <= N)
# def bisect_left(self, a) # B[i] = st.apply(st[:i]) として、Bを値aについて二分探索。挿入位置（左よせ）を返す。同じ値があるときは、その値よりも左の位置を返す。
# def bisect_right(self, a) # B[i] = st.apply(st[:i]) として、Bを値aについて二分探索。挿入位置（左よせ）を返す。同じ値があるときは、その値よりも右の位置を返す。
