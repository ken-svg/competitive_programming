def monotone_minima(f, N, M):
  # argmin_j(f[i][j]) <= argmin_j(f[i+1][j]) のとき、argmin_j(f[i][j])を各i(0 <= i < N-1)について求める
  # 探索範囲は0 <= i < N, 0 <= j < M
  # fは関数で与える(陽にテーブルが与えられる場合はそちらの計算量で律速されるため)
  
  def derive_min(i, l, r): # f(i, j) l <= j < rの範囲を探索
    arg_min = 0
    val_min = f(i, 0)
    for j in range(l, r):
      v = f(i, j)
      if v < val_min:
        arg_min = j
        val_min = v
    return arg_min, val_min
    
  if N == 1:
    arg_min, val_min = derive_min(0, 0, M)
    return [arg_min], [val_min]
  
  ans_arg_min = [None] * N
  ans_val_min = [None] * N
  ans_arg_min[0], ans_val_min[0] = derive_min(0, 0, M)
  
  if N == 1:
    return ans_arg_min, ans_val_min
    
  task = [[N-1, 0, N]]
  while task:
    now_i, pre_i_l, pre_i_r = task.pop()
    j_min = ans_arg_min[pre_i_l]
    j_max = ans_arg_min[pre_i_r] if pre_i_r < N else M-1
    ans_arg_min[now_i], ans_val_min[now_i] = derive_min(now_i, j_min, j_max+1)
    if now_i - pre_i_l > 1:
      next_i = (now_i + pre_i_l) // 2
      task.append([next_i, pre_i_l, now_i])
    if pre_i_r - now_i > 1:
      next_i = (now_i + pre_i_r) // 2
      task.append([next_i, now_i, pre_i_r])
  
  return ans_arg_min, ans_val_min
