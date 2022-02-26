# このページを全て貼り付ける。light_ordered_setは48行目あたりから。

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

class light_ordered_set():
  """ 簡易的な順序集合, 与えた数に近い値を検索するために使う """
  """ c++のstd::setとは異なり、事前にキーの予告が必要。クエリもキーとして予告しておく必要がある。 """
  """ !!! キーは途中で変更できないので注意 !!!"""
  
  """ N: キーの予告 intなら[0, 1, ..., N-1], listなら N自身 """
  """ キーの予告のサイズをSとして、構築：O(SlogS)　検索：O(logS) """
  """ !!! キーがint型以外の場合は78, 79行目をいじること !!! """
  
  def __init__(self, N): # 構築
    if isinstance(N, int):
      A = list(range(N))
    else:
      A = set([i for i in N])
      A = list(A)
      A.sort() 
    self.prepared_keys = A
    # self.key_set = S
    
    # 座標圧縮
    A_inv = {}
    for i, k in enumerate(A):
      A_inv[k] = i
    self.prepared_keys_inv = A_inv
    self.n = len(A)
    
    # unordered set
    self.unordered_set = set()
    
    # min, maxセグメント木の構築
    self.inf = A[-1] + 1 # int 以外の場合はここをいじる
    self.neg_inf = A[0] - 1 # 同上
    self.min_st = SegTree(self.n, op = min, ie = self.inf)
    self.max_st = SegTree(self.n, op = max, ie = self.neg_inf)
    
  def add(self, x): # xを追加
    id_x = self.prepared_keys_inv[x]
    self.min_st.update(id_x, x)
    self.max_st.update(id_x, x)
    self.unordered_set.add(x)
    
  def remove(self, x): # xを削除 
    id_x = self.prepared_keys_inv[x]
    initial = -self.inf
    self.min_st.update(id_x, self.inf)
    self.max_st.update(id_x, self.neg_inf)
    self.unordered_set.remove(x)
    
  def unordered(self): # 通常のsetを返す。イテレーションをしたいときなどに使う。 -> set
    return self.unordered_set
  
  def find(x): # xが入っているなら真、入っていないなら偽 -> bool
    return (x in self.unordered_set)
  
  def left_max(self, x): # xより小さいものの中で最大のもの -> (key) or None
    """ !!! xは最初のkey予告に入れている必要がある !!! """
    id_x = self.prepared_keys_inv[x]
    ans = self.max_st.apply(0, id_x)
    
    return ans if ans > self.neg_inf else None # !! 要素がない場合はNoneとなる !!
    
  def right_min(self, x): # xより大きいものの中で最小のもの -> (key) or None
    """ !!! xは最初のkey予告に入れている必要がある !!! """
    id_x = self.prepared_keys_inv[x]
    ans = self.min_st.apply(id_x+1, self.n)
    
    return ans if ans < self.inf else None # !! 要素がない場合はNoneとなる !!
    
# 例題: ABC217D https://atcoder.jp/contests/abc217/submissions/25897182

  
