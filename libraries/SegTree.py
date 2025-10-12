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
  
  def bisect(self, cond, l = 0): 
    # 条件condを指定すると、cond(apply(l, r))がTrueとなる最大のrを返す。
    # condは以下を満たす:
    # ・cond(apply(l, r))がrについて単調　（例：op = min, cond(x) = [xはある数以上である] ）
    # ・cond(apply(l, l)) = cond(self.ie) = True
    
    v = self.apply(l, self.size)
    if cond(v): return self.n 
    # はじめに、self.apply(l, self.size)を計算。この結果がTrueなら全区間[l, self.n)が答えなのでself.nを返す。
    
    size = self.size; op = self.op; data = self.data;
    now_val = self.ie
    now = l + size
    while now & 1 == 0:
      now >>= 1
    # 左端をlとする最大区間を表すノードから開始。
    
    while True:
      if cond(op(now_val, data[now])): # 現在の区間の分だけ延伸してもcondがTrueのまま
        now_val = op(now_val, data[now])
        now = now + 1
        while now & 1 == 0:
          now >>= 1
        # 右隣へ移動
      else: # 現在の区間を延伸するとFalseとなる
        if now >= size: # 葉ノードであれば、現区間の左端を答えて終了
          return now - size
        
        # そうでなければ、左の子へ移る
        now <<= 1
        
  def bisect_r(self, cond, r): 
    # 条件condを指定すると、cond(apply(l, r))がTrueとなる最小のlを返す。
    # condは以下を満たす:
    # ・cond(apply(l, r))がlについて単調　（例：op = min, cond(x) = [xはある数以上である] ）
    # ・cond(apply(r, r)) = cond(self.ie) = True
    
    v = self.apply(0, r)
    if cond(v): return 0
    # はじめに、self.apply(0, r)を計算。この結果がTrueなら全区間[0, r)が答えなので0を返す。
    
    size = self.size; op = self.op; data = self.data;
    now_val = self.ie
    if r == size:
      now = 1
    else:
      now = r + size
      while now & 1 == 0:
        now >>= 1
      now -= 1
    # 右端をrとする最大区間を表すノードから開始。
    
    while True:
      if cond(op(data[now], now_val)): # 現在の区間の分だけ延伸してもcondがTrueのまま
        now_val = op(data[now], now_val)
        while now & 1 == 0:
          now >>= 1
        now -= 1
        # 左隣へ移動
      else: # 現在の区間を延伸するとFalseとなる
        if now >= size: # 葉ノードであれば、現区間の右端を答えて終了
          return now - size + 1
        
        # そうでなければ、lazyを子へ伝播して、右の子へ移る
        now <<= 1
        now += 1
      
  def __str__(self):
    ans = ["SegmentTree : "]
    def rec(l, r, p, d):
      if r - l > 1:
        c = (r + l) // 2
        rec(l, c, p * 2, d + 1)
      ans.append("_" + "______" * d + "[{:}, {:}) : {:}".format(l, r, self.data[p]))
      if r - l > 1:
        c = (r + l) // 2
        rec(c, r, p * 2 + 1, d + 1)
    rec(0, self.size, 1, 0)    
    return "\n".join(ans)
