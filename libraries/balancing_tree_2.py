class AVL_tree():
  def __init__(self, A):
    self.len = 0
    for a in A:
      self.add(a)
  
  # node = [left, right, value, count, height]
  def _update_info(self, node):
    # update count
    ct = 1
    for d in range(2):
      if node[d] is not None:
        ct += node[d][3]
    node[3] = ct
    # update height
    h = 0
    for d in range(2):
      if node[d] is not None:
        h = max(h, node[d][4] + 1)
    node[4] = h
    
  def _rotate(self, node, dir): # dir = 0 なら右回転, dir = 1なら左回転
    p = node
    q = p[dir]
    if q is None: return p
    r = q[dir ^ 1]
    # dir = 0 のとき q < r < p
    q[dir ^ 1] = p
    p[dir] = r
    
    # update
    self._update_info(p)
    self._update_info(q)
    
    return q # 新しい親ノードを返す
    
  def _double_rotate(self, node, d): # d = 0 なら左回転->右回転, d = 1なら右回転->左回転
    p = node
    q = p[d]
    if q is None: return ""
    r = q[d ^ 1]
    if r is None: return ""
    s = r[d]
    t = r[d ^ 1]
    # d = 0 のとき q < s < r < t < p
    r[d] = q
    r[d ^ 1] = p
    q[d ^ 1] = s
    p[d] = t
    # update
    self._update_info(p)
    self._update_info(q)
    self._update_info(r)
    return r # 新しい親ノードを返す
  
  # node = [left, right, value, count, height]    
  def __contains__(self, x):
    if self.len == 0:
      return False
    now = self.root
    while now is not None:
      if now[2] == x: return True
      else:
        now = now[int(now[2] <= x)]
    return False
  # 上のように、now = now[int(now[2] <= x)]として探索したとき、そのパスは次の性質を持つ
  # 1)辿る最中、所在ノード(now)以下の部分木は、「x以下」と「xより大きい」の境界を必ず含む(両端も考慮する)
  # 2)よって、x以下の最大値と、xより大きい最小値は、存在するなら必ず通る(同じ値については最も右を最大、最も左を最小とする。)
  # 3)とくに、xが存在するなら、必ず通る
  
  def le(self, x):
    if self.len == 0:
      return None
    ans = None
    now = self.root
    while now is not None:
      if now[2] <= x: 
        ans = now[2]
      now = now[int(now[2] <= x)]
    return ans
    
  def rt(self, x):
    if self.len == 0:
      return None
    ans = None
    now = self.root
    while now is not None:
      if now[2] > x: 
        ans = now[2]
      now = now[int(now[2] <= x)]
    return ans
    
  def lt(self, x):
    if self.len == 0:
      return None
    ans = None
    now = self.root
    while now is not None:
      if now[2] < x: 
        ans = now[2]
      now = now[int(now[2] < x)]
    return ans
    
  def re(self, x):
    if self.len == 0:
      return None
    ans = None
    now = self.root
    while now is not None:
      if now[2] >= x: 
        ans = now[2]
      now = now[int(now[2] < x)]
    return ans
    
  def _height_dif(self, node):
    ans = 0
    for d in range(2):
      child = node[d]
      ans += (child[4] if child is not None else -1) * ((-1) ** d) # left_height - right_height
    return ans
    
  def _link(self, par, node, direction):
    # par -> nodeの辺を張る
    if par is not None:
      par[direction] = node
    else:
      self.root = node
    
  def add(self, x):
    if self.len == 0:
      self.root = [None, None, x, 1, 0]
      self.len = 1
      return
    self.len += 1
    now = self.root
    path = []
    direction = [0]
    while now is not None:
      path.append(now)
      d = int(now[2] <= x)
      direction.append(d)
      now = now[d]
    now = path[-1]
    now[direction.pop()] = [None, None, x, 1, 0] # ノード追加
    
    while path:
      now = path.pop()
      d_now = direction.pop() # path[-1] -> nowの方向
      h_dif = self._height_dif(now)
      if abs(h_dif) <= 1:
        self._update_info(now) # 回転しないときは、自分の情報を更新して終わり
        continue
      else:
        unbalance_direction_1 = int(h_dif < 0)
        child = now[unbalance_direction_1]
        if unbalance_direction_1:
          unbalance_direction_2 = int(self._height_dif(child) <= 0)
        else:
          unbalance_direction_2 = int(self._height_dif(child) < 0)
          
        if unbalance_direction_1 == unbalance_direction_2:
          new_node = self._rotate(now, unbalance_direction_1)
        else:
          new_node = self._double_rotate(now, unbalance_direction_1)
        self._link(path[-1] if path else None, new_node, d_now)
        
  def remove(self, x):
    if self.len == 0:
      raise ValueError("key", x, "is not found!!")
      return
    now = self.root
    path = []
    direction = [0]
    target_node = None
    while now is not None:
      path.append(now)
      if now[2] == x:
        target_node = now #最後にnow[2] == xとなったnowが、xの中で最大（最も右）のノード
      d = int(now[2] <= x)
      direction.append(d)
      now = now[d]
    if target_node is None:
      raise ValueError("key", x, "is not found!!")
      return
    
    self.len -= 1
    d = direction.pop()
    now = path.pop()
    child = now[1 ^ d] # Noneではない可能性のあるノード
    if target_node is not now: #nowがxより大きい最小のノードのとき 
      target_node[2] = now[2] # 値の変更
    if not path:
      self.root = child
      return
    now = path[-1] # self.len > 0よりこのnowは必ず存在
    now[direction.pop()] = child # 不要になったノードの削除
    
    self._update_info(now)
    
    while path:
      now = path.pop()
      d_now = direction.pop() # path[-1] -> nowの方向
      h_dif = self._height_dif(now)
      flag = False
      unbalance_direction_1 = None
      unbalance_direction_2 = None
      
      if abs(h_dif) <= 1:
        self._update_info(now) # 回転しないときは、自分の情報を更新して終わり
        
      else:
        unbalance_direction_1 = int(h_dif < 0)
        child = now[unbalance_direction_1]
        if unbalance_direction_1:
          unbalance_direction_2 = int(self._height_dif(child) <= 0)
        else:
          unbalance_direction_2 = int(self._height_dif(child) < 0)
          
        if unbalance_direction_1 == unbalance_direction_2:
          new_node = self._rotate(now, unbalance_direction_1)
        else:
          new_node = self._double_rotate(now, unbalance_direction_1)
        self._link(path[-1] if path else None, new_node, d_now)
        now = new_node
        flag = True
    
  def __getitem__(self, y):
    if not 0 <= y < self.len:
      raise IndexError("index", y, "is out of range 0 to", self.len - 1)
      
    now = self.root
    while True:
      left, right = now[0:2]
      if left is not None:
        if left[3] > y:
          now = left
          continue
        y -= left[3]
      if y == 0:
        return now[2]
      y -= 1
      now = right
  
  def __len__(self):
    return avl_t.len
    
  def __str__(self):
    ans = []
    if self.len == 0:
      return "[]"
    def dfs(node):
      if node[0] is not None:
        dfs(node[0])
      ans.append(node[2])
      if node[1] is not None:
        dfs(node[1])
    dfs(self.root)
    return str(ans)
    
  def listize(self):
    ans = []
    if self.len == 0:
      return ans
    def dfs(node):
      if node[0] is not None:
        dfs(node[0])
      ans.append(node[2])
      if node[1] is not None:
        dfs(node[1])
    dfs(self.root)
    return ans
    
  def _debug(self):
    ans = []
    if self.len == 0:
      return "sort result : []"
    def dfs(node):
      if abs(self._height_dif(node)) >= 2:
        print("balance condition failure at", node[2:], "with h_dif =", self._height_dif(node))
      if node[0] is not None:
        print("left", node[2:], "->", node[0][2:])
        dfs(node[0])
      ans.append(node[2])
      if node[1] is not None:
        print("right", node[2:], "->", node[1][2:])
        dfs(node[1])
    dfs(self.root)
    print("sort result :", ans)
    
avl_t = AVL_tree([0, 6, 4, 5])
avl_t.remove(5)
avl_t.add(7)
avl_t.remove(0)
avl_t.add(12)

print([avl_t[i] for i in range(len(avl_t))])

N, Q = map(int,input().split())
info = []
for _ in range(N):
  s, t, x = map(int,input().split())
  info.append([s - x, -1, x])
  info.append([t - x, -2, x])
  
for q in range(Q):
  d = int(input())
  info.append([d - 0, q, 0])
  
info.sort()
ans = [-1] * Q
avl_t = AVL_tree([])
for dt, t, x in info:
  if t == -1:
    avl_t.add(x)
  elif t == -2:
    avl_t.remove(x)
    
  else:
    y = avl_t.re(x)
    ans[t] = y if y is not None else -1
    
print(*ans, sep = "\n")
