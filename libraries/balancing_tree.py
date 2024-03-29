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
    
    P[q] = pp
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
      
    self._update_H_and_C(p)
    self._update_H_and_C(q)
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
      
    self._update_H_and_C(p)
    self._update_H_and_C(q)
    self._update_H_and_C(r)
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
      
    self._update_H_and_C(p)
    self._update_H_and_C(q)
    self._update_H_and_C(r)
    self._update_H_and_C(pp)
    
  def _left_rotation(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = R[p]
    r = L[q]
    pp = P[p]
    
    P[q] = pp
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
      
    self._update_H_and_C(p)
    self._update_H_and_C(q)
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

class Red_Black_tree():
  def __init__(self, A):
    self.root = None
    """
    self.P = []
    self.L = []
    self.R = []
    self.C = [] # 部分木の頂点数
    self.V = []
    self.IsRed = [] # 赤ならTrue
    以上は最初にaddしたときに作成する
    """
    self.len = 0
    for a in A:
      self.add(a)
      
  def _update_H_and_C(self, node_id):
    if node_id is not None:
      C = self.C
      left = self.L[node_id]
      right = self.R[node_id]
      C[node_id] = 1
      if left is not None:
        C[node_id] += C[left]
      if right is not None:
        C[node_id] += C[right]
        
  def _right_rotation(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = L[p]
    r = R[q]
    pp = P[p]
    
    P[q] = pp
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
      
    self._update_H_and_C(p)
    self._update_H_and_C(q)
    self._update_H_and_C(pp)
  
  def _left_rotation(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = R[p]
    r = L[q]
    pp = P[p]
    
    P[q] = pp
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
      
    self._update_H_and_C(p)
    self._update_H_and_C(q)
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
      
    self._update_H_and_C(p)
    self._update_H_and_C(q)
    self._update_H_and_C(r)
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
      
    self._update_H_and_C(p)
    self._update_H_and_C(q)
    self._update_H_and_C(r)
    self._update_H_and_C(pp)
    
  def _find_greatest_lower(self, x):
    now = self.root
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
  
  def _buttom_up_update_add(self, node_id): # 平衡への復帰、頂点数・高さの更新
    L = self.L
    R = self.R
    P = self.P
    IsRed = self.IsRed
    now = node_id # 必ず赤頂点
    
    while True:
      self._update_H_and_C(now)
      par = P[now]
      if par is None:
        IsRed[now] = False
        break # 根を黒にして終了
      
      if not IsRed[par]: break #平衡条件を満たすので終了
      
      grp = P[par] # 赤頂点の親なので必ず黒
      if L[grp] == par:
        if L[par] == now:
          self._right_rotation(grp)
          IsRed[now] = False
          #IsRed[par] = True 
          #IsRed[grp] = False
          now = par
        else:
          self._left_right_rotation(grp)
          #IsRed[now] = True
          IsRed[par] = False
          #IsRed[grp] = False
          #now = now
      else:
        if L[par] == now:
          self._right_left_rotation(grp)
          #IsRed[now] = True
          IsRed[par] = False 
          #IsRed[grp] = False
          #now = now
        else:
          self._left_rotation(grp)
          IsRed[now] = False
          #IsRed[par] = True 
          #IsRed[grp] = False
          now = par
        
  def add(self, x):
    if self.len == 0:
      self.root = 0
      self.P = [None]
      self.L = [None]
      self.R = [None]
      self.IsRed = [False] # 赤ならTrue
      self.C = [1] # 部分木の頂点数
      self.V = [x]
      self.len = 1
    else:
      self.len += 1
      gl_val, gl_node = self._find_greatest_lower(x)
      P = self.P
      L = self.L
      R = self.R
      IsRed = self.IsRed
      C = self.C
      V = self.V
      
      if gl_node is None: # 追加する値が最小のとき
        now = self.root
        while L[now] is not None:
          now = L[now]
        P.append(now)
        L.append(None)
        R.append(None)
        IsRed.append(True)
        C.append(0)
        V.append(x)
        new_node = len(P) - 1
        L[now] = new_node
        self._buttom_up_update_add(new_node)
        return 
      
      elif R[gl_node] is None:
        # 追加する値が最小でなく(gl_nodeがNoneとならない場合で)
        # gl_nodeの右の子が存在しない場合
        P.append(gl_node)
        L.append(None)
        R.append(None)
        IsRed.append(True)
        C.append(0)
        V.append(x)
        new_node = len(P) - 1
        R[gl_node] = new_node
        self._buttom_up_update_add(new_node)
        return 
      
      else:  
        # gl_nodeの右の子が存在する場合
        now = R[gl_node]
        while L[now] is not None:
          now = L[now] 
        P.append(now)
        L.append(None)
        R.append(None)
        IsRed.append(True)
        C.append(0)
        V.append(x)
        new_node = len(P) - 1
        L[now] = new_node
        self._buttom_up_update_add(new_node)
        return
  
  def _buttom_up_update_remove(self, node_id, par_id): # node_id以下が黒不足（par_idはnode_idの親）のとき、平衡への復帰
    L = self.L
    R = self.R
    P = self.P
    IsRed = self.IsRed
    now = node_id
    par = par_id
    
    while True:
      self._update_H_and_C(now)
      if par is None: # nowが根のとき
        if now is not None:
          IsRed[now] = False
        return # 根を黒にして終了
      
      if L[par] == now: # nowがparの左の子の場合
        right = R[par]
        if right is not None and IsRed[right]: # parの右の子(right)が赤のとき(このとき、parは黒)
          right_left = L[right]
          self._left_rotation(par)
          IsRed[par] = True
          IsRed[right] = False
          right = right_left
          # これで、parの右の子(right)が黒の場合に帰結する
        
        # ここまでの処理により、rightは必ず黒である  
        if right is not None and (L[right] is not None and IsRed[L[right]]): # LP1: rightの左の子が赤のとき
          right_left = L[right]
          self._right_left_rotation(par)
          IsRed[right_left] = IsRed[par]
          IsRed[par] = False
          break # これ以上遡る必要はないので、処理終了
              
        elif right is not None and (R[right] is not None and IsRed[R[right]]): # LP2: rightの右の子が赤のとき
          right_right = R[right]
          self._left_rotation(par)
          IsRed[right] = IsRed[par]
          IsRed[par] = False
          IsRed[right_right] = False
          break # これ以上遡る必要はないので、処理終了
        
        else: # LP3: rightが存在しない時、または、rightの子がいずれも黒の時（子ノードが存在しない場合は黒として扱う）
          p_par_cl = IsRed[par]
          IsRed[par] = False
          if right is not None:
            IsRed[right] = True
          if p_par_cl:
            break # これ以上遡る必要はないので、処理終了
          else:
            now = par
            par = P[par]
            # par以下の黒高さが足りないので、一つ遡って処理を繰り返す
      
      else: # nowがparの右の子の場合
        left = L[par]
        if left is not None and IsRed[left]: # parの左の子(left)が赤のとき(このとき、parは黒)
          left_right = R[left]
          self._right_rotation(par)
          IsRed[par] = True
          IsRed[left] = False
          left = left_right
          # これで、parの左の子(left)が黒の場合に帰結する
        
        # ここまでの処理により、leftは必ず黒である  
        if left is not None and (R[left] is not None and IsRed[R[left]]): # RP1: leftの右の子が赤のとき
          left_right = R[left]
          self._left_right_rotation(par)
          IsRed[left_right] = IsRed[par]
          IsRed[par] = False
          break # これ以上遡る必要はないので、処理終了
              
        elif left is not None and (L[left] is not None and IsRed[L[left]]): # RP2: leftの左の子が赤のとき
          left_left = L[left]
          self._right_rotation(par)
          IsRed[left] = IsRed[par]
          IsRed[par] = False
          IsRed[left_left] = False
          break # これ以上遡る必要はないので、処理終了
          
        else: # RP3: leftが存在しない時、または、leftの子がいずれも黒の時（子ノードが存在しない場合は黒として扱う）
          p_par_cl = IsRed[par]
          IsRed[par] = False
          if left is not None:
            IsRed[left] = True
          if p_par_cl:
            break # これ以上遡る必要はないので、処理終了
          else:
            now = par
            par = P[par]
            # par以下の黒高さが足りないので、一つ遡って処理を繰り返す
          
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
      IsRed = self.IsRed
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
        if not IsRed[gl_node]: # 除去した点が黒のとき
          self._buttom_up_update_remove(right, par)
        
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
        p_left_cl = IsRed[left]
        IsRed[left] = IsRed[gl_node]
        if not p_left_cl: # 除去した点が黒のとき
          self._buttom_up_update_remove(L[left], left)
        
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
        p_now_cl = IsRed[now]
        IsRed[now] = IsRed[gl_node]
        
        #nowがあった場所の周囲を更新(nowの元親は必ず存在し、nowの元右の子は存在しないことに注意)
        R[now_par] = now_left # nowはもともと右の子だった
        if now_left is not None:
          P[now_left] = now_par
        
        if not p_now_cl: # 除去した点が黒のとき  
          self._buttom_up_update_remove(now_left, now_par)
        
  def __contains__(self, x):
    gl_val, gl_node = self._find_greatest_lower(x)
    return gl_node is not None and x == gl_val
    
  def __str__(self):
    now = self.root
    P = self.P
    L = self.L
    R = self.R
    V = self.V
    IsRed = self.IsRed
    ans = []
    state = {}
    while now is not None:
      if now not in state:
        state[now] = 1
        if L[now] is not None:
          print("left", now, "->", L[now], " color", IsRed[now], "->", IsRed[L[now]])
          now = L[now]
          
      elif state[now] == 1:
        state[now] = 2
        ans.append(V[now])
        if R[now] is not None:
          print("right", now, "->", R[now], " color", IsRed[now], "->", IsRed[R[now]])
          now = R[now]
          
      else:
        now = P[now]
    return str(ans)

from random import randint
class Treap():
  def __init__(self, A):
    self.root = None
    """
    self.P = []
    self.L = []
    self.R = []
    self.W = [] # 重さ（優先度）
    self.C = [] # 部分木の頂点数
    self.V = []
    以上は最初にaddしたときに作成する
    """
    self.len = 0
    for a in A:
      self.add(a)
      
  def _update_H_and_C(self, node_id):
    if node_id is not None:
      C = self.C
      left = self.L[node_id]
      right = self.R[node_id]
      C[node_id] = 1
      if left is not None:
        C[node_id] += C[left]
      if right is not None:
        C[node_id] += C[right]
        
  def _right_rotation(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = L[p]
    r = R[q]
    pp = P[p]
    
    P[q] = pp
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
      
    self._update_H_and_C(p)
    self._update_H_and_C(q)
    self._update_H_and_C(pp)
  
  def _left_rotation(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = R[p]
    r = L[q]
    pp = P[p]
    
    P[q] = pp
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
      
    self._update_H_and_C(p)
    self._update_H_and_C(q)
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
  
  def _buttom_up_update_add(self, node_id): # 平衡への復帰、頂点数・高さの更新
    L = self.L
    R = self.R
    P = self.P
    W = self.W
    now = node_id
    
    while now is not None:
      self._update_H_and_C(now)
      par = P[now]
      if par is None: break
    
      if W[par] > W[now]:
        if L[par] == now:
          self._right_rotation(par)
        else:
          self._left_rotation(par)
        self._update_H_and_C(par)
      else:
        break
        
  def add(self, x):
    if self.len == 0:
      self.root = 0
      self.P = [None]
      self.L = [None]
      self.R = [None]
      self.W = [randint(1, 10**6)] # 重さ（優先度）
      self.C = [1] # 部分木の頂点数
      self.V = [x]
      self.len = 1
    else:
      self.len += 1
      gl_val, gl_node = self._find_greatest_lower(x)
      P = self.P
      L = self.L
      R = self.R
      W = self.W
      C = self.C
      V = self.V
      
      if gl_node is None: # 追加する値が最小のとき
        now = self.root
        while L[now] is not None:
          now = self.L[now]
        P.append(now)
        L.append(None)
        R.append(None)
        W.append(randint(1, 10**6))
        C.append(0)
        V.append(x)
        new_node = len(P) - 1
        L[now] = new_node
        self._buttom_up_update_add(new_node)
        return 
      
      elif R[gl_node] is None:
        # 追加する値が最小でない場合で、
        # gl_nodeの右の子が存在しない場合
        P.append(gl_node)
        L.append(None)
        R.append(None)
        W.append(randint(1, 10**6))
        C.append(0)
        V.append(x)
        new_node = len(P) - 1
        R[gl_node] = new_node
        self._buttom_up_update_add(new_node)
        return 
      
      else:  
        # gl_nodeの右の子が存在する場合
        now = R[gl_node]
        while L[now] is not None:
          now = L[now] 
        P.append(now)
        L.append(None)
        R.append(None)
        W.append(randint(1, 10**6))
        C.append(0)
        V.append(x)
        new_node = len(P) - 1
        L[now] = new_node
        self._buttom_up_update_add(new_node)
        return
  
  def _move_down_and_remove(self, node_id): # 削除対象の頂点を葉へ移動し、削除
    L = self.L
    R = self.R
    P = self.P
    W = self.W
    now = node_id
    
    path = []
    while True:
      left = L[now]
      right = R[now]
      if left is None and right is None:
        # 削除
        par = P[now]
        if par is not None:
          if L[par] == now:
            L[par] = None
          else:
            R[par] = None
        break
      if right is None or (left is not None and W[left] < W[right]):
        path.append(left)
        self._right_rotation(now)
      else:
        path.append(right)
        self._left_rotation(now)
        
    for p in path[::-1]:
      self._update_H_and_C(p)
      
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
      self._move_down_and_remove(gl_node)
      
  def __contains__(self, x):
    gl_val, gl_node = self._find_greatest_lower(x)
    return gl_node is not None and x == gl_val
    
  def __str__(self):
    now = self.root
    P = self.P
    L = self.L
    R = self.R
    V = self.V
    W = self.W
    ans = []
    state = {}
    while now is not None:
      if now not in state:
        state[now] = 1
        if L[now] is not None:
          print("left", now, "->", L[now], " priority", W[now], "->", W[L[now]])
          now = L[now]
          
      elif state[now] == 1:
        state[now] = 2
        ans.append(V[now])
        if R[now] is not None:
          print("right", now, "->", R[now], " priority", W[now], "->", W[R[now]])
          now = R[now]
          
      else:
        now = P[now]
    return str(ans)

class Splay_tree():
  def __init__(self, A):
    self.root = None
    """
    self.P = []
    self.L = []
    self.R = []
    self.C = [] # 部分木の頂点数
    self.V = []
    以上は最初にaddしたときに作成する
    """
    self.len = 0
    for a in A:
      self.add(a) 
      
  def _update_H_and_C(self, node_id):
    if node_id is not None:
      C = self.C
      left = self.L[node_id]
      right = self.R[node_id]
      C[node_id] = 1
      if left is not None:
        C[node_id] += C[left]
      if right is not None:
        C[node_id] += C[right]
        
  def _zig(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = P[p]
    if q is None: return # 親がいないので、zigできない
    pp = P[q]
    
    if L[q] == p:
      r = R[p]
      if r is not None:
        P[r] = q
      L[q] = r
      R[p] = q
      P[q] = p
      P[p] = pp
      if pp is None:
        self.root = p
      else:
        if L[pp] == q:
          L[pp] = p
        else:
          R[pp] = p
      
    else:
      r = L[p]
      if r is not None:
        P[r] = q
      R[q] = r
      L[p] = q
      P[q] = p
      P[p] = pp
      if pp is None:
        self.root = p
      else:
        if L[pp] == r:
          L[pp] = p
        else:
          R[pp] = p
    self._update_H_and_C(q) 
    self._update_H_and_C(p)
  
          
  def _zig_zig(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = P[p]
    if q is None: return # 親がいないので、zigできない
    r = P[q]
    if r is None: return # 祖がいないので、zig_zigできない
    pp = P[r]
    if L[q] == p and L[r] == q:
      s = R[p]
      t = R[q]
      L[r] = t
      if t is not None:
        P[t] = r
      L[q] = s
      if s is not None:
        P[s] = q
      P[r] = q
      R[q] = r
      P[q] = p
      R[p] = q
      P[p] = pp
      if pp is None:
        self.root = p
      else:
        if L[pp] == r:
          L[pp] = p
        else:
          R[pp] = p
      
    elif R[q] == p and R[r] == q:
      s = L[p]
      t = L[q]
      R[r] = t
      if t is not None:
        P[t] = r
      R[q] = s
      if s is not None:
        P[s] = q
      P[r] = q
      L[q] = r
      P[q] = p
      L[p] = q
      P[p] = pp
      if pp is None:
        self.root = p
      else:
        if L[pp] == r:
          L[pp] = p
        else:
          R[pp] = p
    
    self._update_H_and_C(r) 
    self._update_H_and_C(q) 
    self._update_H_and_C(p)
      
  def _zig_zag(self, node_id):
    P = self.P
    R = self.R
    L = self.L
    p = node_id
    q = P[p]
    if q is None: return # 親がいないので、zigできない
    r = P[q]
    if r is None: return # 祖がいないので、zig_zigできない
    pp = P[r]
    if R[q] == p and L[r] == q:
      s = L[p]
      t = R[p]
      R[q] = s
      if s is not None:
        P[s] = q
      L[r] = t
      if t is not None:
        P[t] = r
      L[p] = q
      P[q] = p
      R[p] = r
      P[r] = p
      P[p] = pp
      if pp is None:
        self.root = p
      else:
        if L[pp] == r:
          L[pp] = p
        else:
          R[pp] = p
    
    if L[q] == p and R[r] == q:
      s = R[p]
      t = L[p]
      L[q] = s
      if s is not None:
        P[s] = q
      R[r] = t
      if t is not None:
        P[t] = r
      R[p] = q
      P[q] = p
      L[p] = r
      P[r] = p
      P[p] = pp
      if pp is None:
        self.root = p
      else:
        if L[pp] == r:
          L[pp] = p
        else:
          R[pp] = p  
    
    self._update_H_and_C(r) 
    self._update_H_and_C(q) 
    self._update_H_and_C(p)
  
  def _splay(self, node_id):
    P = self.P
    L = self.L
    R = self.R
    while (P[node_id] is not None):
      p = node_id
      q = P[p]
      r = P[q]
      if r is None:
        self._zig(p)
      elif L[r] == q:
        if L[q] == p:
          self._zig_zig(p)
        else:
          self._zig_zag(p)
      else:
        if R[q] == p:
          self._zig_zig(p)
        else:
          self._zig_zag(p)
    
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
    if node_found is not None:
      self._splay(node_found)
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
    if node_found is not None:
      self._splay(node_found)
    return val, node_found # 値、頂点(、値以上の要素数)を返す
  
  def add(self, x):
    if self.len == 0:
      self.root = 0
      self.P = [None]
      self.L = [None]
      self.R = [None]
      self.C = [1] # 部分木の頂点数
      self.V = [x]
      self.len = 1
      return
    
    P = self.P
    L = self.L
    R = self.R
    C = self.C
    V = self.V
    new_node = len(self.P)
    self.len += 1
    _, gl_node = self._find_greatest_lower(x)
    if gl_node is None:
      _, lu_node = self._find_least_upper(x)
      P.append(None)
      R.append(lu_node)
      L.append(None)
      V.append(x)
      C.append(0)
      self.root = new_node
      P[lu_node] = new_node
      self._update_H_and_C(new_node)
      
    else:
      P.append(None)
      L.append(gl_node)
      R.append(R[gl_node])
      if R[gl_node] is not None:
        P[R[gl_node]] = new_node
      R[gl_node] = None
      V.append(x)
      C.append(0)
      self.root = new_node
      P[gl_node] = new_node
      self._update_H_and_C(gl_node)
      self._update_H_and_C(new_node)
      
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
      C = self.C
      V = self.V
      
      target = self.root
      left = L[target]
      right = R[target]
      if left is None:
        self.root = right
        P[right] = None
      elif R[left] is None:
        self.root = left
        P[left] = None
        if right is not None:
          P[right] = left
        R[left] = right
        self._update_H_and_C(left)
      else:
        now = left
        while R[now] is not None:
          now = R[now]
        now_left = L[now]
        now_par = P[now]
        # nowの削除(nowの値はtarget(root)へ)
        R[now_par] = now_left
        if now_left is not None:
          P[now_left] = now_par
        V[target] = V[now]
        now = now_par
        while True:
          self._update_H_and_C(now)
          if P[now] is not None: break
          now = P[now]
        
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
          print("left", now, "->", L[now])
          now = L[now]
          
      elif state[now] == 1:
        state[now] = 2
        ans.append(V[now])
        if R[now] is not None:
          print("right", now, "->", R[now])
          now = R[now]
          
      else:
        now = P[now]
    return str(ans)  
