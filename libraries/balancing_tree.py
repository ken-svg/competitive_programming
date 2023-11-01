class AVL_tree():
  def __init__(self, A):
    self.root = None
    """
    self.P = []
    self.L = []
    self.R = []
    self.H = [] # 高さ
    self.C = [] # 部分木の頂点数
    self.V = []
    以上は最初にaddしたときに作成する
    """
    self.len = 0
    for a in A:
      self.add(a)
      
  def _update_H_and_C(self, node_id):
    if node_id is not None:
      H = self.H
      C = self.C
      left = self.L[node_id]
      right = self.R[node_id]
      C[node_id] = 1
      H[node_id] = 0
      if left is not None:
        C[node_id] += C[left]
        H[node_id] = max(H[node_id], H[left] + 1)
      if right is not None:
        C[node_id] += C[right]
        H[node_id] = max(H[node_id], H[right] + 1)
        
  def _right_rotation(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = L[p]
    r = R[q]
    pp = P[p]
    
    P[q] = P[p]
    R[q] = p
    P[p] = q
    L[p] = r
    if r is not None:
      P[r] = p
    if pp is not None:
      if L[pp] == p:
        L[pp] = q
      else:
        R[pp] = q
    else:
      self.root = q
      
    self._update_H_and_C(q)
    self._update_H_and_C(p)
    self._update_H_and_C(pp)
  
  def _left_right_rotation(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = L[p]
    r = R[q]
    s = L[r]
    t = R[r]
    pp = P[p]
    
    P[r] = pp
    R[r] = p
    L[r] = q
    P[p] = P[q] = r
    R[q] = s
    L[p] = t
    if s is not None:
      P[s] = q
    if t is not None:
      P[t] = p
    if pp is not None:
      if L[pp] == p:
        L[pp] = r
      else:
        R[pp] = r
    else:
      self.root = r
      
    self._update_H_and_C(r)
    self._update_H_and_C(q)
    self._update_H_and_C(p)
    self._update_H_and_C(pp)
    
  def _right_left_rotation(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = R[p]
    r = L[q]
    s = R[r]
    t = L[r]
    pp = P[p]
    
    P[r] = pp
    L[r] = p
    R[r] = q
    P[p] = P[q] = r
    L[q] = s
    R[p] = t
    if s is not None:
      P[s] = q
    if t is not None:
      P[t] = p
    if pp is not None:
      if L[pp] == p:
        L[pp] = r
      else:
        R[pp] = r
    else:
      self.root = r
      
    self._update_H_and_C(r)
    self._update_H_and_C(q)
    self._update_H_and_C(p)
    self._update_H_and_C(pp)
    
  def _left_rotation(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = R[p]
    r = L[q]
    pp = P[p]
    
    P[q] = P[p]
    L[q] = p
    P[p] = q
    R[p] = r
    if r is not None:
      P[r] = p
    if pp is not None:
      if L[pp] == p:
        L[pp] = q
      else:
        R[pp] = q
    else:
      self.root = q
      
    self._update_H_and_C(q)
    self._update_H_and_C(p)
    self._update_H_and_C(pp)
  
  def _find_greatest_lower(self, x):
    now = self.root
    if now is None:
      return None, None
    V = self.V
    L = self.L
    R = self.R
    C = self.C
    val, node_found = None, None
    count = C[now] if now is not None else 0
    while now is not None:
      if x < V[now]:
        count -= 1
        if R[now] is not None:
          count -= C[R[now]]
        now = L[now]
      else:
        val, node_found = V[now], now
        now = R[now]
    return val, node_found # 値、頂点(、値以下の要素数)を返す
    
  def _find_least_upper(self, x):
    now = self.root
    if now is None:
      return None, None
    V = self.V
    L = self.L
    R = self.R
    C = self.C
    val, node_found = None, None
    count = C[now] if now is not None else 0
    while now is not None:
      if V[now] < x:
        count -= 1
        if L[now] is not None:
          count -= C[L[now]]
        now = R[now]
      else:
        val, node_found = V[now], now
        now = L[now]
    return val, node_found # 値、頂点(、値以上の要素数)を返す
  
  def _buttom_up_update(self, node_id): # 平衡への復帰、頂点数・高さの更新
    L = self.L
    R = self.R
    P = self.P
    H = self.H
    now = node_id
    
    while now is not None:
      self._update_H_and_C(now)
      left = L[now]
      right = R[now]
      H_left = H[left] if left is not None else -1
      H_right = H[right] if right is not None else -1
      
      # 平衡条件が破れた場合に回転を行う
      if H_left - H_right > 1:
        left_left = L[left]
        left_right = R[left]
        H_left_left = H[left_left] if left_left is not None else -1
        H_left_right = H[left_right] if left_right is not None else -1
        if H_left_left - H_left_right >= 0:
          self._right_rotation(now)
        else:
          self._left_right_rotation(now) 
          
      elif H_right - H_left > 1:
        right_left = L[right]
        right_right = R[right]
        H_right_left = H[right_left] if right_left is not None else -1
        H_right_right = H[right_right] if right_right is not None else -1
        if H_right_right - H_right_left >= 0:
          self._left_rotation(now)
        else:
          self._right_left_rotation(now) 
        
      now = P[now]
        
  def add(self, x):
    if self.len == 0:
      self.root = 0
      self.P = [None]
      self.L = [None]
      self.R = [None]
      self.H = [0] # 高さ(葉の場合は0)
      self.C = [1] # 部分木の頂点数
      self.V = [x]
      self.len = 1
    else:
      self.len += 1
      gl_val, gl_node = self._find_greatest_lower(x)
      P = self.P
      L = self.L
      R = self.R
      H = self.H
      C = self.C
      V = self.V
      
      if gl_node is None: # 追加する値が最小のとき
        now = self.root
        while L[now] is not None:
          now = self.L[now]
        P.append(now)
        L.append(None)
        R.append(None)
        H.append(0)
        C.append(0)
        V.append(x)
        new_node = len(P) - 1
        L[now] = new_node
        self._buttom_up_update(new_node)
        return 
      
      elif R[gl_node] is None:
        # 追加する値が最小でなく、gl_nodeがNoneとならない場合で、
        # gl_nodeの右の子が存在しない場合
        P.append(gl_node)
        L.append(None)
        R.append(None)
        H.append(0)
        C.append(0)
        V.append(x)
        new_node = len(P) - 1
        R[gl_node] = new_node
        self._buttom_up_update(new_node)
        return 
      
      else:  
        # gl_nodeの右の子が存在する場合
        now = R[gl_node]
        while L[now] is not None:
          now = L[now] 
        P.append(now)
        L.append(None)
        R.append(None)
        H.append(0)
        C.append(0)
        V.append(x)
        new_node = len(P) - 1
        L[now] = new_node
        self._buttom_up_update(new_node)
        return
      
  def remove(self, x):
    if self.len == 0:
      print("AVL_tree.remove: not found " + str(x) + " !!")
      return 
    else:
      gl_val, gl_node = self._find_greatest_lower(x)
      if x != gl_val:
        print("AVL_tree.remove: not found " + str(x) + " !!")
        return
      self.len -= 1
      if self.len == 0:
        self.root = None
        return
      P = self.P
      L = self.L
      R = self.R
      H = self.H
      C = self.C
      V = self.V
      
      if L[gl_node] is None:
        # 左の子が存在しない場合
        right = R[gl_node]
        par = P[gl_node]
        if right is not None:
          P[right] = par
        if par is None:
          self.root = right
        else:
          if R[par] == gl_node:
            R[par] = right
          else:
            L[par] = right
        if right is not None:  
          self._buttom_up_update(right)
        else:
          self._buttom_up_update(par)
        
      elif R[L[gl_node]] is None:
        # 左の子は存在するが、そのさらに右の子が存在しない場合
        left = L[gl_node]
        right = R[gl_node]
        par = P[gl_node]
        P[left] = par
        R[left] = right
        if right is not None:
          P[right] = left
        if par is None:
          self.root = left
        else:
          if R[par] == gl_node:
            R[par] = left
          else:
            L[par] = left
        self._buttom_up_update(left)
        
      else:
        # 左の子以下の頂点のうち、最大のものを求める
        left = L[gl_node]
        right = R[gl_node]
        par = P[gl_node]
        now = R[left]
        while R[now] is not None:
          now = R[now]
        
        #gl_nodeの周囲を更新
        P[left] = now  
        if right is not None:
          P[right] = now
        if par is None:
          self.root = now
        else:
          if R[par] == gl_node:
            R[par] = now
          else:
            L[par] = now
        
        #nowをgl_nodeの位置に組み込む    
        now_left = L[now]
        now_par = P[now]
        P[now] = par
        L[now] = left
        R[now] = right
        
        #nowがあった場所の周囲を更新(nowの元親は必ず存在し、nowの元右の子は存在しないことに注意)
        R[now_par] = now_left # nowはもともと右の子だった
        if now_left is not None:
          P[now_left] = now_par
        
        if now_left is not None:
          self._buttom_up_update(now_left)
        else:
          self._buttom_up_update(now_par)
        
  def __contains__(self, x):
    gl_val, gl_node = self._find_greatest_lower(x)
    return gl_node is not None and x == gl_val
    
  def __str__(self):
    now = self.root
    P = self.P
    L = self.L
    R = self.R
    V = self.V
    ans = []
    state = {}
    while now is not None:
      if now not in state:
        state[now] = 1
        if L[now] is not None:
          #print("left", now, "->", L[now])
          now = L[now]
          
      elif state[now] == 1:
        state[now] = 2
        ans.append(V[now])
        if R[now] is not None:
          #print("right", now, "->", R[now])
          now = R[now]
          
      else:
        now = P[now]
    return str(ans)
