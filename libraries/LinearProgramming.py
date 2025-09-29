def LP_Simplex(A, b, c):
  # 単体法による線形計画問題の求解。
  # 制約 Ax <= b, 目的 max{cx}
  # 最適値と解の一つ（基底解）を出力
  
  # 初期構築
  N = len(c)
  M = len(b)
  
  offset = [abs(v) for v in b] # 基底変数（最初なのでスラック変数を用意）
  neg = [i for i in range(M) if b[i] < 0] # b[i]が負の場合、１段階目用にスラック変数の符号を反転する。それを記録。
  coef = [[-v for v in a] for a in A] # 係数行列（基底変数を非基底変数で表したときの係数）
  for i in neg:
    coef[i] = [-v for v in coef[i]] # 符号反転
  
  var_id = [k for k in range(N + M)] # 変数の入れ変えを管理
  for phase in range(1, 3):
    if not neg and phase == 1: continue
    if neg and phase == 2: # 2段階目はスラック変数の符号を正に統一
      neg_set = set([i + N for i in neg])
      for k, v in enumerate(var_id):
        if v < N or (v not in neg_set): continue
        if k < N:
          for coef_i in coef:
            coef_i[k] *= -1
        else:
          coef[k - N] = [-v for v in coef[k - N]]
          offset[k - N] *= -1
      
    # コストの初期化
    cost = [0] * N
    cost_offset = 0
    if phase == 1: # 第一段階　負座標の削除
      for i in neg:
        coef_i = coef[i]
        for j in range(N):
          cost[j] -= coef_i[j]
        cost_offset -= offset[i]
    else:
      for k, v in enumerate(var_id):
        if v >= N: continue
        if k < N:
          cost[k] += c[v]
        else:
          c_v = c[v]
          coef_ = coef[k - N]
          for j in range(N):
            cost[j] += coef_[j] * c_v
          cost_offset += offset[k - N] * c_v
          
    # 求解
    while any(v > 0 for v in cost):
      
      max_val_j = None
      arg_j = None
      arg_i = None
        
      for j in range(N):
        if cost[j] <= 0: continue
        
        min_val_i = None
        tmp_i = None
        for i in range(M):
          if coef[i][j] >= 0: continue
          v = abs(offset[i] / coef[i][j])
          if (min_val_i is None) or (min_val_i > v):
            min_val_i = v
            tmp_i = i
            
        if min_val_i is None:
          return "Unbounded"
          
        upd = cost[j] * min_val_i
            
        if (max_val_j is None) or (max_val_j < upd):  
          max_val_j = upd
          arg_j = j
          arg_i = tmp_i
      
      
      j = arg_j # 基底変数に追加
      i = arg_i # 基底変数から追い出し
      
      d = abs(coef[i][j])
      coef_i = coef[i]
      
      coef[i] = [coef_i[k] / d if k != j else -1 / d for k in range(N)]
      offset[i] = offset[i] / d
      
      coef_i = coef[i]
      offset_i = offset[i]
      for k in range(M):
        if k == i: continue
        coef_k = coef[k]
        q = coef_k[j]
        coef_k[j] = 0
        for l in range(N):
          coef_k[l] += q * coef_i[l]
        offset[k] += q * offset_i
        
      cost_j = cost[j]
      cost[j] = 0
      for l in range(N):
        cost[l] += cost_j * coef_i[l]
      cost_offset += cost_j * offset_i
          
      var_id[i + N], var_id[j] = var_id[j], var_id[i + N]
      #print(coef, offset, cost, cost_offset, i, j, var_id)
             
        
  sol = [0] * N
  for k, v in enumerate(var_id[N:]):
    if v < N:
      sol[v] = offset[k]
      
  return cost_offset, sol
