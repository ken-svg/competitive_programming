class LazySegTree():
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
    
  def action(self, l, r, x): # 半開区間[l,r)にxを作用
    if l >= r: return 
    row_num = self.size.bit_length() # 行数(深さ)
    # 1, 伝搬（トップダウン）
    #self._topdown(l, r) 
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
        
    # 2, 作用（ボトムアップ）
    #self._bottomup_action(l, r, x)
    _pop = self._pop; _upd = self._upd;
    row_num = self.size.bit_length() # 行数(深さ)
    #l += self.size; r += self.size
    
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
        
  def apply(self, l, r): # 半開区間[l,r)の計算結果
    if l >= r: return self.ie
    # 1, 伝搬（トップダウン）
    #self._topdown(l, r)
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
    
    # 2, 計算（ボトムアップ）
    #return self._bottomup_apply(l, r)
    size = self.size; op = self.op; data = self.data;
    #r += size; l += size
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
    #print(v)
    if cond(v): return self.n 
    # はじめに、self.apply(l, self.size)を計算。この結果がTrueなら全区間[l, self.n)が答えなのでself.nを返す。
    # この計算により、lの直上のノードにおけるlazyはすべてクリアされる。
    
    size = self.size; op = self.op; data = self.data; _push = self._push;
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
        
        # そうでなければ、lazyを子へ伝播して、左の子へ移る
        _push(now)
        now <<= 1
        
  def bisect_r(self, cond, r): 
    # 条件condを指定すると、cond(apply(l, r))がTrueとなる最小のlを返す。
    # condは以下を満たす:
    # ・cond(apply(l, r))がlについて単調　（例：op = min, cond(x) = [xはある数以上である] ）
    # ・cond(apply(r, r)) = cond(self.ie) = True
    
    v = self.apply(0, r)
    #print(v)
    if cond(v): return 0
    # はじめに、self.apply(0, r)を計算。この結果がTrueなら全区間[0, r)が答えなので0を返す。
    # この計算により、rの直上のノードにおけるlazyはすべてクリアされる。
    
    size = self.size; op = self.op; data = self.data; _push = self._push;
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
        _push(now)
        now <<= 1
        now += 1
      
  def __str__(self):
    ans = ["LazySegmentTree : "]
    def rec(l, r, p, d):
      #print(p, self.size, l, r, self.data[p])
      if r - l > 1:
        c = (r + l) // 2
        rec(l, c, p * 2, d + 1)
      if p < self.size and self.lazy[p] != self.ic:
        ans.append("_" + "______" * d + "[{:}, {:}) : {:} (act:{:})".format(l, r, self.data[p], self.lazy[p]))
      else:
        ans.append("_" + "______" * d + "[{:}, {:}) : {:}".format(l, r, self.data[p]))
      if r - l > 1:
        c = (r + l) // 2
        rec(c, r, p * 2 + 1, d + 1)
    rec(0, self.size, 1, 0)    
    return "\n".join(ans)
