# このページをすべて貼り付けること！
# 入っているもの
# suffix_array(S)
# lcp_array(S, sa)

def suffix_array(S):
  # 入力： 英小文字列or数列S, 出力： 接尾辞配列 sa (0...N-1の順列)
  # ※ 接尾辞配列sa:
  #    [S[sa[i]:N-1] for i in range(N)]が辞書式順序で昇順となる
  
  # SA-IS法
  # O(NlogN + K) where N = len(S), K = 文字種列or最大値-最小値
  
  if len(S) < 10: # サイズの小さい場合はO(N(logN)^2)を使う
    return _sa_log(S)  
  
  if isinstance(S, str):
    S = [ord(s) for s in S]
  S_max = max(S)
  S_min = min(S)
  S = [s - S_min + 1 for s in S]
  K = S_max - S_min + 1 + 1

  S.append(0) # 番兵
  
  task = []
  type_info = []
  bin_info = []
  
  #induced sort-1(wrong sort)
  while len(S) > 1:
    N = len(S)
    
    # S型(S[i] < S[i+1])か否かの判定 -> is_typeS (list[bool])
    is_typeS = [True] 
    for i in range(N-2,-1,-1):
      if S[i] != S[i+1]:
        is_typeS.append(S[i] < S[i+1])
      else:
        is_typeS.append(is_typeS[-1])
    is_typeS.reverse()
    type_info.append(is_typeS)
    
    # LMSの列挙(昇順) -> LMS (list[int])
    LMS = []
    is_L = True
    for i in range(N):
      if is_L and is_typeS[i]:
        LMS.append(i)
      is_L = not(is_typeS[i])
    
    # LMSの座標圧縮 -> LMS_pos (list[int])
    # 添字iがidx番目のLMSの場合、LMS_pos[idx]=iとなるようにする
    LMS_pos = []
    for i in LMS:
      LMS_pos.append(i)
    
    # bin(頭文字とtypeごとの分布区間)の把握 
    #  -> bin_seg_left, bin_seg_right 左端, 右端 (list[int], list[int])
    bin_seg_left = []
    bin_seg_right = []
    ct = [0]*(2*K)
    for s in S: 
      if is_typeS[i]: #S型は奇数で管理
        ct[(s<<1) | 1] += 1
      else: #L型は偶数で管理
        ct[(s<<1)] += 1
      tmp = 0
    for c in range(2*K):
      bin_seg_left.append(tmp)
      bin_seg_right.append(tmp+ct[c]-1)
      tmp += ct[c]
    
    # 情報蓄積
    task.append([S, is_typeS, LMS_pos, bin_seg_left, bin_seg_right])
    
    # induced sort-1
    pre_sa = _induced_sort(S, is_typeS, LMS[::-1], bin_seg_left, bin_seg_right, step1_normal_order = True)
    
    # 次のinduced sort-1のため、S[i:LMS_next[i]]の辞書順を、pre_saから求める
    # 各LMSについて、次のLMSを把握
    LMS_next = {} 
    prv = LMS[0]
    for i in LMS[1:]:
      LMS_next[prv] = i
      prv = i
    LMS_next[prv] = N
    
    #「LMSではない」かどうかをbool値で -> not_LMS_bool(list[bool])
    not_LMS_bool = [True]*N
    for i in LMS:
      not_LMS_bool[i] = False
    
    order = [-1]*N #順番の記載
    idx = -1
    tmp = None
    for i in pre_sa: 
      if not_LMS_bool[i]: continue
      # LMSを順番に確保
      val = S[i:LMS_next[i]]
      if tmp != val:
        idx += 1
        tmp = val
      order[i] = idx # 辞書順を数値に変換して記憶
    order = [idx for idx in order if idx >= 0]
    S = order
    K = idx+1 # 文字種の数を更新
    
      
  #induced sort-2(correct sort)
  task.pop()
  while task:
    
    # 情報の更新
    S, is_typeS, LMS_pos, bin_seg_left, bin_seg_right = task.pop()
    N = len(S)
    
    # 前のSのpre_saについて、LMSの順番を辞書順に
    LMS_order = [LMS_pos[idx] for idx in pre_sa] 
    
    pre_sa = _induced_sort(S, is_typeS, LMS_order, bin_seg_left, bin_seg_right)
    
  return pre_sa

def _induced_sort(S, is_typeS, LMS, bin_seg_left, bin_seg_right, step1_normal_order = False):
  # S:対象, is_typeS:S型か否か(list[bool]), LMS:LMS開始位置のリスト(list[int])
  # bin_seg_left: 各binの左端(list[int]), bin, bin_seg_right: 各binの右端(list[int])
  # LMSのリストが辞書順で与えられる場合に正しいsaを返す
  N = len(S)
  K = len(bin_seg_left)>>1 #文字種の数
  ct = [0]*(K<<1)
  pre_sa = [None]*N #Sから決まる
  
  #Step1: LMSの仮パッキング (通常は逆順に走査)
  if step1_normal_order: #正順に走査(wrong induced sortの時に使用)
    for l in LMS: 
      c = (S[l]<<1) | 1
      pre_sa[bin_seg_right[c] - ct[c]] = l
      ct[c] += 1
    for c in range(1,K<<1,2): ct[c] = 0  
  else: #逆順に走査
    for l in LMS[::-1]: 
      c = (S[l]<<1) | 1
      pre_sa[bin_seg_right[c] - ct[c]] = l
      ct[c] += 1
    for c in range(1,K<<1,2): ct[c] = 0  
  
  #Step2: L型のパッキング(saを正順に走査、その値-1がL型の場合にbinに埋める)
  for v in pre_sa: 
    if v == None or v == 0 or is_typeS[v-1]: continue
    c = (S[v-1]<<1)
    pre_sa[bin_seg_left[c] + ct[c]] = v-1
    ct[c] += 1
  idx = -1 
  
  #Step3: S型のパッキング(saを逆順に走査、その値-1がS型の場合にbinに埋める)
  while idx >= -N:
    v = pre_sa[idx]
    idx -= 1
    if v == 0 or not(is_typeS[v-1]): continue
    c = (S[v-1]<<1) | 1
    pre_sa[bin_seg_right[c] - ct[c]] = v-1
    ct[c] += 1
  
  return pre_sa
  
def _sa_log(S): # O(N(logN)^2)の解法。 サイズの小さいときはこちらを使う
  if isinstance(S, str):
    S = [ord(s) for s in S]
  S_max = max(S)
  S_min = min(S)
  S = [s - S_min + 1 for s in S]
  K = S_max - S_min + 1 + 1
  S.append(0)
  
  N = len(S)
  
  pre_ans = S
  
  def conv(a, b, c):
    return (a * (2*N+1) + b) * N + c
  def inv(info):
    info2 = info // N
    a = info2 // (2*N+1)
    b = info2 % (2*N+1)
    c = info % N
    return a, b, c
  
  interval = 0
  while interval < N:
    to_be_sorted = []
    for i in range(N-interval):
      to_be_sorted.append(conv(pre_ans[i], pre_ans[i+interval], i))
    for i in range(N-interval, N):
      to_be_sorted.append(conv(pre_ans[i], 0, i))
    to_be_sorted.sort()
    del pre_ans
    pre_ans = [-1]*N
    idx = -1
    p1, p2 = -2, -2
    for info in to_be_sorted:
      k1, k2, i = inv(info)
      if not(p1 == k1 and p2 == k2):
        idx += 1
        p1, p2 = k1, k2
      pre_ans[i] = idx
    if interval == 0: interval = 1
    else: interval <<= 1
  
  return [inv(info)[2] for info in to_be_sorted]

def lcp_array(S, sa):
  # 高さ配列 (i番目の要素がS[sa[i]..n) と S[sa[i+1]..n)の最長共通接頭辞の長さ)
  # 入力: S 文字列/リスト, sa suffix array (!! 空文字列を含まない !!)
  N = len(S)
  
  inv_sa = [0]*N
  
  for i, a in enumerate(sa):
    inv_sa[a] = i
  
  ans = [0]*N
  tmp_ans = 0
  common_len = 0
  for i in range(N):
    if inv_sa[i] == N-1: continue
    i_next_on_sa = sa[inv_sa[i] + 1]
    
    while common_len < N-i and S[i+common_len] == S[i_next_on_sa+common_len]:
      common_len += 1  
    ans[inv_sa[i]] = common_len
    
    if common_len > 0:
      common_len -= 1
    
  return ans

