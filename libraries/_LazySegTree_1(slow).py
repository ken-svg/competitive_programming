class LazySegTree():
  """ 入出力はすべて0-idx"""
  """ n: 要素数 """
  """ ベースモノイド op: 結合律を満たす演算(モノイド), ie: モノイド演算opの単位元  """
  """ 作用         cp: 結合律を満たす演算(作用),   ic: 作用演算opの単位元 """
  """             act(x,a): モノイドの元xにaが作用                   """
  def __init__(self, n, op, ie, cp, ic, act):
    self.n = n
    self.size = 1 << (n-1).bit_length()
    self.op = op; self.ie = ie;
    self.data = [ie]*(2*self.size) #1以降が有効データ, 桁数で階層を表現
    self.cp = cp; self.ic = ic; self.act = act;
    self.lazy = [ic]*(self.size) #lazy
    
  def construct(self, A): # Aを初期値として構成 0(nlog(n))
    n = min(self.n,len(A))
    data = self.data; size = self.size; op = self.op;
    data[size:size+n] = A[:n]
    for i in range(size-1,0,-1):
      j = i << 1
      data[i] = op(data[j], data[j+1])  
      
  def _push(self, now):
    lazy_now = self.lazy[now]
    if lazy_now == self.ic: return
    
    lazy = self.lazy; data = self.data;
    cp = self.cp; act = self.act;
    
    des = now << 1 #左下のノード 
    data[des] = act(data[des], lazy_now)
    data[des+1] = act(data[des+1], lazy_now)
    if des < self.size:
      lazy[des] = cp(lazy[des], lazy_now)
      lazy[des+1] = cp(lazy[des+1], lazy_now)
    lazy[now] = self.ic
  
  def _pop(self, now):
    data = self.data;
    data[now] = self.op(data[now<<1], data[(now<<1)+1])
  
  def _upd(self, now, x):
    self.data[now] = self.act(self.data[now], x)
    if now < self.size: self.lazy[now] = self.cp(self.lazy[now], x)
      
  def _topdown(self, l, r): # 1, 伝搬処理(共通)
    _push = self._push
    row_num = self.size.bit_length() # 行数(深さ)
    l += self.size; r += self.size
    
    l_now = 1; r_now = 2;
    for d in range(row_num-1): # dを桁数とする
      sft = row_num - 1 - d #シフトすべき桁数
      if l != l_now << sft: 
        _push(l_now) #左側の伝搬
      if r != r_now << sft: 
        _push(r_now-1) #右側の伝搬  
      l_now <<= 1; r_now <<= 1;
      if (l >> (sft-1)) != l_now:     l_now += 1
      if ((r-1) >> (sft-1)) != r_now-1:  r_now -= 1
  
  def _bottomup_action(self, l, r, x):
    _pop = self._pop; _upd = self._upd;
    row_num = self.size.bit_length() # 行数(深さ)
    l += self.size; r += self.size
    
    l1 = l; l2 = l; r1 = r; r2 = r; 
    #[l1,r1):計算中の区間, [l2,r2):まだxを反映していない区間
    
    # 更新
    while l2 < r2: #区間[l2,r2)が残っていないときはこの処理を行わない
      if l2 & 1: _upd(l2, x); l2 += 1
      if r2 & 1: _upd(r2-1, x); r2 -= 1
      l2 >>= 1; r2 >>= 1;
    
    # 上へ再計算
    for d in range(row_num-2,-1,-1): # dを桁数とする
      sft = row_num - 1 - d
      if l != (l >> sft) << sft: _pop(l >> sft)   # 左側の計算
      if r != (r >> sft) << sft: _pop((r-1) >> sft) # 右側の計算
  
  def _bottomup_apply(self, l, r):
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
    
  def action(self, l, r, x): # 半開区間[l,r)にxを作用
    if l >= r: return 
    row_num = self.size.bit_length() # 行数(深さ)
    # 1, 伝搬（トップダウン）
    self._topdown(l, r) 
    # 2, 作用（ボトムアップ）
    self._bottomup_action(l, r, x)
    
  def apply(self, l, r): # 半開区間[l,r)の計算結果
    if l >= r: return self.ie
    # 1, 伝搬（トップダウン）
    self._topdown(l, r) 
    # 2, 計算（ボトムアップ）
    return self._bottomup_apply(l, r)
