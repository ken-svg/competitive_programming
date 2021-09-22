class ordered_set():
  # 同じ数を挿入した場合、重複はカウントされない
  
  def __init__(self):
    self.unordered_set = set()
    self.inf = 1 << 62
    self.root = [self.inf, None, None, 0] 
    # nodeは[値, 左の子, 右の子, 高さ] で表す
    
  def find(self, x):
    return x in self.unordered_set
  
  def left_max(self, x): # x以下の最大のもの
    if x in self.unordered_set: return x
    p = self.root
    l = -self.inf
    r = self.inf
    while True:
      v = p[0]
      if x < v: # 左に下る
        p = p[1]
        r = v
      else: # 右に下る
        p = p[2]
        l = v
      if p is None:
        return l if l > -self.inf else None
        
  def right_min(self, x): # x以上の最小のもの
    if x in self.unordered_set: return x
    p = self.root
    l = -self.inf
    r = self.inf
    while True:
      v = p[0]
      if x < v: # 左に下る
        p = p[1]
        r = v
      else: # 右に下る
        p = p[2]
        l = v
      if p is None:
        return r if r < self.inf else None  
  
  def _right_rotate(self, p, pp, direction): # 左が重いとき
    # p : 回転で降下する頂点、pp: pの親頂点 
    # direction: pがppのどちら向きの子か(左ならTrue, 右ならFalse)
    
    q = p[1]
    r = q[2]
    
    # ppの更新
    if direction: # pがppの左子のとき
      pp[1] = q # 左子の更新
    else:
      pp[2] = q # 右子の更新
    pplh = 0 if pp[1] is None else pp[1][3] + 1
    pprh = 0 if pp[2] is None else pp[2][3] + 1
    pp[3] = max(pplh, pprh)
      
    # pの更新
    p[1] = r
    plh = 0 if r is None else r[3] + 1
    prh = 0 if p[2] is None else p[2][3] + 1 
    p[3] = max(plh, prh)
    
    # qの更新
    q[2] = p
    qlh = 0 if q[1] is None else q[1][3] + 1
    qrh = 0 if p is None else p[3] + 1 
    q[3] = max(qlh, qrh)
    
  def _left_rotate(self, p, pp, direction): # 右が重いとき
    # p : 回転で降下する頂点、pp: pの親頂点 
    # direction: pがppのどちら向きの子か(左ならTrue, 右ならFalse)
    
    q = p[2]
    r = q[1]
    
    # ppの更新
    if direction: # pがppの左子のとき
      pp[1] = q # 左子の更新
    else:
      pp[2] = q # 右子の更新
    pplh = 0 if pp[1] is None else pp[1][3] + 1
    pprh = 0 if pp[2] is None else pp[2][3] + 1
    pp[3] = max(pplh, pprh)
      
    # pの更新
    p[2] = r
    plh = 0 if p[1] is None else p[1][3] + 1
    prh = 0 if p[2] is None else p[2][3] + 1 
    p[3] = max(plh, prh)
    
    # qの更新
    q[1] = p
    qlh = 0 if q[1] is None else q[1][3] + 1
    qrh = 0 if q[2] is None else q[2][3] + 1 
    q[3] = max(qlh, qrh)    
    
  def add(self, x):
    p = self.root
    
    # 探索
    path = [p]
    directions = []
    while True:
      v = p[0]
      if v == x: return # 値が重複するので更新しない
      elif x < v: # 左に下る
        if p[1] is None:
          p[1] = [x, None, None, 0]
          break
        p = p[1]
        path.append(p)
        directions.append(True)
      else: # 右に下る
        if p[2] is None:
          p[2] = [x, None, None, 0]
          break
        p = p[2]
        path.append(p)
        directions.append(False)
    
    self.unordered_set.add(x)
    
    # 中間結果
    # p: 新たに追加した頂点の親
    # path: rootからpまでの道
    # directions: 道の途中で進んだ方向の記録
    
    # 平衡
    for i in range(len(directions)-1, -1, -1):
      p = path[i+1]
      
      plh = 0 if p[1] is None else p[1][3] + 1
      prh = 0 if p[2] is None else p[2][3] + 1
      
      if prh == plh + 2:
        q = p[2]
        qlh = 0 if q[1] is None else q[1][3] + 1
        qrh = 0 if q[2] is None else q[2][3] + 1
        if qlh > qrh: # 下の頂点の左側が重たい場合(right-left case)
          self._right_rotate(q, p, directions[i+1])  
        pp = path[i]
        self._left_rotate(p, pp, directions[i])
        break # 挿入の場合は、もとと高さが変わらないはずなので終了
        
      elif plh == prh + 2:
        q = p[1]
        qlh = 0 if q[1] is None else q[1][3] + 1
        qrh = 0 if q[2] is None else q[2][3] + 1
        if qrh > qlh: # 下の頂点の左側が重たい場合(left-right case)
          self._left_rotate(q, p, directions[i+1])  
        pp = path[i]
        self._right_rotate(p, pp, directions[i])
        break
        
      elif prh == plh: # 高さが変わらないなら終了
        break
        
      p[3] = max(prh, plh)
    
      
   
  def show(self):
    root = self.root
    showing = [None]
    
    task = [(1, root)]
    while task:
      task_next = []
      for p, node in task:
        
        while len(showing) <= p:
          showing.append(None)
        showing[p] = [node[0], node[3]]
          
        
        if node[1] is not None:
          task_next.append((p << 1, node[1]))
        if node[2] is not None:
          task_next.append(((p << 1) | 1, node[2]))
          
      task = task_next
      task_next = []
      
    V = 1 << (len(showing)-1).bit_length()
    while len(showing) < V:
      showing.append(None)
    #print(showing)
    V = (len(showing) >> 1)
    #print(V)
    j = 2
    for m in range(1, V.bit_length()):
      show_line = [None] * V
      for i in range(0, V, V>>m):
        show_line[i] = showing[j]
        j += 1
        #print(i,j)
      print(show_line[:len(show_line)>>1])
