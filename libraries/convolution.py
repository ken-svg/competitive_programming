# 注意：
# 1,convolutionを行うには、以下を全て貼り付けること
# 2,より高精度（値が大きい場合）な計算のため、オプション値roots, modsをいろいろ試すこと

# 数論変換（フーリエ変換の有限体上での実装）
def _Number_Theorem_transformation(A, mod, root, inv = False):
  # 配列Aを最小の２べきに拡張(0fill)したもののフーリエ変換を、素数modを法とする有限体上で求める。
  # inv: Trueなら逆変換, mod:素数の法, root: 原始根
  # デフォルト値について 469762049 = 7*(2^26) + 1, 30^(2^26) = 1 より、2^26までのデータサイズを扱える。
  # 順変換、逆変換ともに【規格化していない】ので注意（順変換→逆変換と繰り返すと、len(A)以上最小の2べき倍された値が出てくる）
  
  if inv:
    # 逆元準備
    _inv_t = {}
    _inv_t[1] = 1
    _inv_t[0] = 0
    def inv_f(x, mod):
      if x not in _inv_t:
        _inv_t[x] = inv_f(mod % x, mod) * (mod - mod // x) % mod
      return _inv_t[x]
    root = inv_f(root, mod)
   
  # 原始根のべきの準備
  N_t = len(A)
  B = (N_t-1).bit_length() 
  R = [root]  
  for j in range(100):
    R_next = pow(R[-1], 2, mod)
    if R_next == 1: break
    if j == 50:
      return "Error: Root is inappropriate." 
      # rootの周期が長すぎる、または２べきでないため、なかなか１にならない
    R.append(pow(R[-1], 2, mod))
  if B >= len(R): 
    return "Error: Data size is too big." 
    # データサイズがrootの周期に対して大きすぎる
  # 原始根べき
  R = [1] + R[len(R)-1:len(R)-B-1:-1] # R[i] = (1の原始2^i乗根)
  r = R[-1]
    
  # 初期配列の準備
  N = 1<<B
  idx_set = [0]
  dif = 1<<(B-1)
  while len(idx_set) < N:
    for i in range(len(idx_set)):
      idx_set.append(idx_set[i] + dif)
    dif >>= 1
  S = [A[i] if i < N_t else 0 for i in idx_set]  
  
  # バタフライ演算
  section = 2
  idx = 1
  while section <= N:
    # １段ごとの操作
    base = 0 # ブロックのはじめ
    half = section >> 1 # ブロックの真ん中
    r = R[idx] # 現在の段における根
    factor = 1 # 加算時の第２項の係数
    S_next = []
    
    for i in range(N):
      S_next.append((S[base + (i % half)] + factor * S[base + half + (i % half)]) % mod)
      # ↑バタフライ演算の本体
      
      # 更新処理
      factor *= r # 係数更新
      factor %= mod
      if i == base + section - 1: #次のブロックへ
        base += section
    section <<= 1 #1ブロックサイズを倍に
    del S
    S = S_next
    idx += 1
  
  return S

# 拡張ユークリッド互除法 (詳細はnumbersへ)
def ext_gcd(a, b):
  flag = False
  if abs(b) > abs(a): 
    a, b = b, a
    flag = True
  if b == 0:
    if flag: 
      if a < 0: return 0, -1, -a
      else: return 0, 1, a
    if a < 0: return -1, 0, -a
    return 1, 0, a
  xp, yp, d = ext_gcd(b, a % b)
  x = yp
  y = xp - (a//b) * yp
  if flag:
    x, y = y, x
  return x, y, d

def convolution(A, B, mods = [998244353], roots = [15311432]): # 配列AとBの畳み込みを返す
  # より高精度なオプションの例： mods = [469762049, 2013265921, 167772161], roots = [30, 137, 17]
  # 注意： ext_gcd, _Number_Theorem_transformationを要求する。これらを同時に貼り付けること。
  # inv: Trueなら逆変換, mod:素数の法(リストで複数与えることも可能), root: 原始根(リストで複数与えることも可能,modも同じ長さのリスト)
  # デフォルト値について 469762049 = 7*(2^26) + 1, 30^(2^26) = 1 より、2^26までのデータサイズを扱える。
  
  if isinstance(mods, int) and isinstance(roots, int): mods = [mods]; roots = [roots]
  elif not(isinstance(mods, list) and isinstance(roots, list) and len(roots) == len(mods)):
    print("Error : mods and roots should be given as lists with same length!") # オプションの入力ミス
    return None
  
  ABs = []
  NA = len(A)
  NB = len(B)
  V = NA + NB
  for i in range(len(mods)):
    mod = mods[i]; root = roots[i];
    
    Ac = [A[i] if i < NA else 0 for i in range(V)]
    Bc = [B[i] if i < NB else 0 for i in range(V)]
    FA = _Number_Theorem_transformation(Ac, mod, root)
    FB = _Number_Theorem_transformation(Bc, mod, root)

    if isinstance(FA, str): print("NTT :", FA, "at", mod, root)
    if isinstance(FB, str): print("NTT :", FB, "at", mod, root)
    if isinstance(FA, str) or isinstance(FB, str): return None # 数論変換が失敗した場合
    
    # 逆元準備
    _inv_t = {}
    _inv_t[1] = 1
    _inv_t[0] = 0
    def inv_f(x, mod):
      if x not in _inv_t:
        _inv_t[x] = inv_f(mod % x, mod) * (mod - mod // x) % mod
      return _inv_t[x]

    V = len(FA)
    V_inv = inv_f(V, mod)
    FAB = [FA[i] * FB[i] for i in range(V)]
    ABc = _Number_Theorem_transformation(FAB, mod, root, inv = True)[:NA + NB-1]
    ABc = [(a * V_inv) % mod for a in ABc]
    ABs.append(ABc)
  
  AB_ans = ABs[0]
  # CRTを使って再構成
  mod0 = mods[0]
  for i in range(1,len(ABs)):
    AB_next = ABs[i]
    mod1 = mods[i]
    if mod0 % mod1 == 0: continue
    x, y, _ = ext_gcd(mod0, mod1) # x * mod0 + y * mod1 = 1:
    for j in range(len(AB_ans)):
      AB_ans[j] = (AB_ans[j]*y*mod1 + AB_next[j]*x*mod0) % (mod0*mod1)
    mod0 *= mod1
  AB_ans = [((a + (mod0>>1)) % mod0) - (mod0>>1) for a in AB_ans]
  return AB_ans

# 使用例： https://atcoder.jp/contests/atc001/submissions/20033938
