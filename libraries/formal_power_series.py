mod = 998244353
Fac = [1, 998244352, 911660635, 372528824, 929031873, 452798380, 922799308, 781712469, 476477967, 166035806, 258648936, 584193783, 63912897, 350007156, 666702199, 968855178, 629671588, 24514907, 996173970, 363395222, 565042129, 733596141, 267099868, 15311432]
Fiv = [1, 998244352, 86583718, 509520358, 337190230, 87557064, 609441965, 135236158, 304459705, 685443576, 381598368, 335559352, 129292727, 358024708, 814576206, 708402881, 283043518, 3707709, 121392023, 704923114, 950391366, 428961804, 382752275, 469870224]

# mod = 素数
_inv_t = {}
_inv_t[1] = 1
_inv_t[0] = 0
def inv(x, mod):
  x %= mod
  if x not in _inv_t:
    _inv_t[x] = inv(mod % x, mod) * (mod - mod // x) % mod
  return _inv_t[x]

def _root_yield(r = 15311432, c = 23):
  global Fac, Fiv
  if r != 15311432 or  c != 23 or mod != 998244353:
    Fac = [r]
    Fiv = [inv(r, mod)]
    for i in range(c):
      Fac.append((Fac[-1] ** 2) % mod)
      Fiv.append((Fiv[-1] ** 2) % mod)
    Fac.reverse()
    Fiv.reverse()
      
  Fac_3 = [pow(f_inv, 3, mod) for f_inv in Fiv]
  Root = [Fac[2]]
  for f_inv_3 in Fac_3[3:]:
    Root.append((Root[-1] * f_inv_3) % mod)
  Root_inv = [inv(root, mod) for root in Root]
  return Root, Root_inv      

Root, Root_inv = _root_yield()

def _butterfly(A):
  N = len(A)
  B = N.bit_length() - 1
  
  for b in range(B):
    section_size = 1 << (B - b)
    section_num = 1 << b
    section_size_half = section_size >> 1
    fac = 1
    for s in range(section_num):
      section_base = s << (B - b)
      for i in range(section_size_half):
        Ap = A[section_base + i]
        Am = A[section_base + i + section_size_half] * fac
        A[section_base + i] = (Ap + Am) % mod
        A[section_base + i + section_size_half] = (Ap - Am) % mod
        
      fac *= Root[(~s & -(~s)).bit_length() - 1]
      fac %= mod

def _butterfly_inv(A):
  N = len(A)
  B = N.bit_length() - 1
  
  for b in range(B-1, -1, -1):
    section_size = 1 << (B - b)
    section_num = 1 << b
    section_size_half = section_size >> 1
    fac_inv = 1
    for s in range(section_num):
      section_base = s << (B - b)
      for i in range(section_size_half):
        Ap = A[section_base + i]
        Am = A[section_base + i + section_size_half]
        A[section_base + i] = (Ap + Am) % mod
        A[section_base + i + section_size_half] = ((Ap - Am) * fac_inv) % mod
        
      fac_inv *= Root_inv[(~s & -(~s)).bit_length() - 1]
      fac_inv %= mod 
      
def fps_power(A, B): # A * B
  NP = len(A) + len(B) - 1
  N = 1 << (NP-1).bit_length()
  N_inv = inv(N, mod)
  A = [(a * N_inv) % mod for a in A] + [0] * (N - len(A))
  B = [b for b in B] + [0] * (N - len(B))
  _butterfly(A)
  _butterfly(B)
  C = [(fa * fb) % mod for fa, fb in zip(A, B)]
  _butterfly_inv(C)
  return C

def fps_inv(A, length): # 1 / A, length-1次まで求める
  if A[0] == 0:
    print("<fps_inv: Zero division!>")
  G = [inv(A[0], mod)]
  A_neg = [-A[i] for i in range(min(len(A), length))]
  if length > len(A_neg):
    A_neg += [0] * (length - len(A))
  now_len = 1
  while now_len < length:
    next_len = min(length, now_len << 1)
    H = fps_power(G, A_neg[:next_len])[now_len:next_len]
    G[len(G):] = fps_power(G, H)[:next_len-now_len]
    now_len = next_len
  return G

def polynomial_div(A, B): # A // B
  A = [a for a in A]
  B = [b for b in B]
  while A[-1] == 0:
    A.pop()
  while B[-1] == 0:
    B.pop()
  if len(B) == 0:
    print("<polynomial_div: Zero division!>")
  if len(A) < len(B):
    return [0]
  N = len(A) - len(B) + 1
  C = fps.power(A[::-1], B[::-1])[N-1::-1]
  return C

def fps_dif(A): # dA / dx
  return [(A[i] * i) % mod for i in range(1, len(A))]
def fps_int(A): # \int (A dx)
  ans = [0]
  for i in range(len(A)):
    ans.append((A[i] * inv(i+1, mod)) % mod)
  return ans

def fps_log(A, length): # log(A), Aは定数項が[1], length-1次まで
  if A[0] != 1:
    print("<fps_log> First term is not 1! ({})".format(A[0])); return;
  A_inv = fps_inv(A, length)
  A_dif = fps_dif(A)
  return fps_int(fps_power(A_inv, A_dif)[:length-1])

def fps_exp(A, length): # exp(A), Aは定数項が[0], length-1次まで
    if A[0] != 0:
      print("<fps_exp> First term is not 0! ({})".format(A[0])); return;
    G = [1]
    # gn = gp(f + 1 - log(gp))
    now_len = 1
    while now_len < length:
      next_len = min(now_len << 1, length)
      G_dif = [(g * i) % mod for i, g in enumerate(G) if i > 0] + [0]
      G_neg = [-g for g in G]
      if now_len == 1: 
        G_inv = [1]
      else:
        G_inv = G_inv[:now_len >> 1]
        H = fps_power(G_inv, G_neg)[now_len >> 1:now_len]
        G_inv[len(G_inv):] = fps_power(G_inv, H)[:now_len >> 1]
      H = (fps_power(G_inv, G_neg) + [0])[now_len:next_len]
      G_inv[len(G_inv):] = fps_power(G_inv[:next_len-now_len], H)[:next_len-now_len]
      V = fps_power(G_dif, G_inv)
      H = [((A[i] if i < len(A) else 0) - V[i-1] * inv(i, mod)) % mod for i in range(now_len, next_len)]
      G[now_len:] = fps_power(G, H)[:next_len - now_len]
      now_len = next_len
      #print(G)
    return G
  
# ----- 以下は没案、当初はfpsをclassで実装する方針だった -----

def convolution(conved_list):
  total_length = 1
  for A in conved_list:
    total_length += (len(A) - 1)
  
  B = (total_length - 1).bit_length()
  N = (1 << B)
  
  conved_list_copy = [[a for a in A] + [0] * (N - len(A)) for A in conved_list]
  for A in conved_list_copy:
    _butterfly(A)
  
  multiplied = [1] * N
  for A in conved_list_copy:
    for i in range(N):
      multiplied[i] *= A[i]
      multiplied[i] %= mod
      
  _butterfly_inv(multiplied)
  N_inv = inv(N, mod)
  return [(multiplied[i] * N_inv) % mod for i in range(total_length)]

Deg_inf = 1 << 50
class fps(): #形式的冪級数
  def __init__(self, A, precision = Deg_inf, head_sft = 0): 
    # 入力 : x^{head_sft} * (A(x) + O(x^{precision}))
    values = []
    if isinstance(A, list):
      values = [[i + head_sft, a % mod] for i, a in enumerate(A) if a % mod and i < precision]
    elif isinstance(A, dict):
      values = [[i + head_sft, a % mod] for i, a in A.items() if a % mod and i < precision]
    elif isinstance(A, int):
      values = [[head_sft, A % mod]] if A % mod and 0 < precision else []
    self.A = {}
    if values:
      self.head = head = min([i for i, a in values])
      for i, a in values:
        self.A[i - head] = a
        self.precision = precision + head_sft - head if precision < Deg_inf else Deg_inf
    else:
      self.precision = precision
      self.head = 0
    # 出力の例：precision=2, head=3なら A(x) = x^3 * (a + bx + O(x^2))
      
  def __eq__(self, other): # 等号
    return (self.precision == other.precision) and (self.A == other.A)
  def __nq__(self, other): # 不等号
    return (self.precision != other.precision) or (self.A != other.A)
  def __add__(self, other, neg = 1): # 加算
    head = min(self.head, other.head)
    tail = min(self.head + self.precision, other.head + other.precision)
    precision = tail - head
    if min(self.precision, other.precision) == Deg_inf:
      preicion = Deg_inf
    head_A = self.head
    A, B = self.A, other.A
    C = {}
    for i, a in A.items():
      im = i + head_A - head
      if i + head_A < tail:
        C[im] = a
    head_B = other.head
    for j, b in B.items():
      jm = j + head_B - head
      if jm < tail:
        if jm in C: C[jm] = (C[jm] + b * neg) % mod 
        else: C[jm] = (b * neg) % mod
    return fps(C, precision = precision, head_sft = head)
  def __iadd__(self, other):
    return self.__add__(other)
  def __sub__(self, other): # 減算
    return self.__add__(other, neg = -1)
  def __isub__(self, other):
    return self.__add__(other, neg = -1)
  def _list_form(self, A):
    A_list = []
    for i, a in A.items():
      A_list += [0] * (max(i+1 - len(A_list), 0))
      A_list[i] = a
    return A_list    
  def __mul__(self, other): # 乗算
    precision = min(self.precision, other.precision)
    head_sft = self.head + other.head
    if len(self.A) < 16 or len(other.A) < 16:
      A = self.A
      B = other.A
      C = {}
      for a, v in A.items():
        for b, w in B.items():
          c = a + b
          if c not in C:
            C[c] = (v * w) % mod
          else:
            C[c] += (v * w) % mod
      return fps(C, precision = precision, head_sft = head_sft)
    A_list = self._list_form(self.A)
    B_list = other._list_form(other.A)
    precision = min(self.precision, other.precision)
    return fps(convolution([A_list[:precision], B_list[:precision]]), precision = precision, head_sft = head_sft)
  def __imul__(self, other):
    return __mul__(self, other)
  def _inv_list(self, A, length):
    if length > 10 ** 6:
      print("<fps : _inv_list> length of inv_list is too large ({})!".format(length)); return;
    if length > len(A):
      A += [0] * (length - len(A))
    if length == 0: return []
    G = [inv(A[0], mod)]
    now_len = 1
    A_neg = [-a for a in A]
    while now_len < length:
      next_len = min(length, now_len << 1)
      H = convolution([G, A_neg[:next_len]])[now_len:next_len]
      G += convolution([G, H])[:next_len-now_len]
      now_len = next_len
    return G
  def inv(self, max_precision = min(Deg_inf, 10**6), sparse_num = 50):
    if len(self.A) == 0:
      print("<fps : inv> Zero division!"); return;
    if len(self.A) < sparse_num:
      return self.__truediv__(1, self, max_precision = max_precision, sparse_num = sparse_num)
    A_list = self._list_form(self.A)
    head_sft = -self.head
    precision = min(max_precision, self.precision)
    A_list_inv = self._inv_list(A_list, length = precision)
    return fps(A_list_inv, precision = precision, head_sft = head_sft)
  def __truediv__(self, other, max_precision = min(Deg_inf, 10**6), sparse_num = 50):
    # precision　は　10^6を限界としている
    if len(other.A) == 0:
      print("<fps : truediv> Zero division!"); return;
    if len(self.A) == 0:
      return fps(0, precision = min(self.precision, other.precision))
    A_list = self._list_form(self.A)
    B_list = other._list_form(other.A)
    head_sft = self.head - other.head
    precision = min(self.precision, other.precision, max_precision)
    if len(other.A) < sparse_num:
      R = A_list + [0] * max(0, precision - len(A_list))
      if len(R) > precision: R = R[:precision]
      B = other.A
      b0_inv = inv(B[0], mod)
      C = []
      for i in range(precision):
        v = (R[i] * b0_inv) % mod
        C.append(v)
        for j, w in B.items():
          if i + j < precision:
            R[i+j] = (R[i+j] - (v * w)) % mod
      return fps(C, precision = precision, head_sft = head_sft)  
    B_list_inv = self._inv_list(B_list, length = precision)
    C = convolution([A_list[:precision], B_list_inv])
    return fps(C, precision = precision, head_sft = head_sft)
  def __floordiv__(self, other): 
    if len(other.A) == 0:
      print("<fps : floordiv> Zero division!"); return;
    precision = min(self.precision, other.precision)
    if precision < Deg_inf:
      print("<fps : floordiv> Input is not polinomial! (precision != inf)"); return;
    if min(self.head, other.head) < 0:
      print("<fps : floordiv> Input is not polinomial! (includes negative power)"); return;
    A_list = self._list_form(self.A)
    B_list = other._list_form(other.A)
    A_deg = self.head + len(A_list) - 1
    B_deg = other.head + len(B_list) - 1
    length = A_deg - B_deg + 1
    if length <= 0:
      return fps(0)
    A_list_rev = A_list[-1:-length-1:-1]
    B_list_rev = B_list[-1:-length-1:-1]
    B_list_rev_inv = self._inv_list(B_list_rev, length = length)
    C = convolution([A_list_rev, B_list_rev_inv])[length-1::-1]
    return fps(C)
  def __mod__(self, other):
    print(self, ((self // other) * other))
    return self - ((self // other) * other)
  def integrate(self, inplace = False):
    B = {}
    head = self.head
    for i, a in self.A.items():
      j = i + head
      if j != -1:
        B[i] = (a * inv(j+1, mod)) % mod
      else:
        print("<fps : integrate> include (-1)-times power with coefficient = {}".format(a)); return;
    if inplace: 
      self.A = B
      self.head = head + 1
      return self
    else:
      return fps(B, precision = self.precision, head_sft = head + 1)
  def differentiate(self, inplace = False):
    B = {}
    pre_head = self.head
    head = pre_head - 1
    if pre_head == 0:
      head = min([i + pre_head - 1 for i, a in self.A.items() if i != 0])
    for i, a in self.A.items():
      j = i + pre_head
      if j != 0:
        B[j - 1 - head] = (a * j) % mod
    if inplace:
      if pre_head == 0:
        if self.precision < Deg_inf:
          self.precision -= head - (pre_head - 1)
        self.A = B
        self.head = head
        return self
    else:
      return fps(B, precision = self.precision - (head - (pre_head - 1)) if self.precision < Deg_inf else Deg_inf, head_sft = head)
  def log(self): # 最小次数の項が「１」であること
    if self.head != 0:
      print("<fps : log> First term is not \"1\"! (coef * x^{})".format(self.head)); return;
    A = self.A
    if A[0] != 1:
      print("<fps : log> First term is not \"1\"! ({})".format(self.head)); return;
    return (self.differentiate() / self).integrate()
  def exp(self): # 定数項より次数の低い項を含まないこと
    if self.head < 0:
      print("<fps : exp> include negative power!"); return;
    if self.head == 0:
      print("<fps : exp> include constant!"); return;
    A_list = [0] * self.head + self._list_form(self.A)
    A_list += [0] * (self.precision + self.head - len(A_list))
    G = [1]
    precision = self.head + self.precision
    # gn = gp(f + 1 - log(gp))
    now_len = 1
    while now_len < precision:
      next_len = min(now_len << 1, precision)
      G_dif = [(g * i) % mod for i, g in enumerate(G) if i > 0] + [0]
      G_neg = [-g for g in G]
      if now_len == 1: 
        G_inv = [1]
      else:
        G_inv = G_inv[:now_len >> 1]
        H = convolution([G_inv, G_neg])[now_len >> 1:now_len]
        G_inv += convolution([G_inv, H])[:now_len >> 1]
      H = (convolution([G_inv, G_neg]) + [0])[now_len:next_len]
      G_inv += convolution([G_inv[:next_len-now_len], H])[:next_len-now_len]
      #G_inv = self._inv_list(G, length = next_len-1)
      #print(G_inv)
      #G_log = [0] + [(g * inv(i+1, mod)) % mod for i, g in enumerate(convolution([G_dif, G_inv])[:next_len-1])]
      V = convolution([G_dif, G_inv])
      H = [(A_list[i] - V[i-1] * inv(i, mod)) % mod for i in range(now_len, next_len)]
      G[now_len:next_len] = convolution([G, H])[:next_len - now_len]
      now_len = next_len
      #print(G)
    return fps(G, precision = precision, head_sft = 0)
  def power(self, k):
    if len(self.A) == 0: return fps(0, precision = self.precision)
    base_head = self.head
    base_coef = self.A[0]
    c = self / fps({0 : base_coef}, precision = self.precision, head_sft = base_head)
    return (c.log() * fps(k)).exp() * fps({0 : pow(base_coef, k, mod)}, precision = self.precision, head_sft = k * base_head)
  
  def __str__(self):
    rtn = ["x^{} * (".format(self.head)]
    if self.A == {}:
      rtn += ["0 + "]
    else:
      for i, a in sorted([[i, a] for i, a in self.A.items()]):
        a = (a + mod // 2) % mod - mod // 2
        rtn += ["{}*x^{} + ".format(a if a > 0 else "({})".format(a), i if i >= 0 else "({})".format(i))]
    rtn += ["O(x^{}))".format(self.precision if self.precision < Deg_inf else "inf")]
    return "".join(rtn)
  def shift(self, step):
    if step == 0:
      return self
    if self.head < 0:
      print("<fps : shift> include negative power!"); return;
    if self.precision < Deg_inf:
      print("<fps : shift> precision is not inf of {}".format(self.precision)); return;
    A_list = []
    now_len = 0
    for i, v in self.A.items():
      j = i + self.head
      if j > 10 ** 6:
        print("<fps : shift> include too learge degree of {}".format(j)); return;
      while now_len <= j:
        A_list.append(now_len)
        now_len += 1
      A_list[j] = v
    max_deg = len(A_list) - 1
    factor = 1
    for j in range(max_deg + 1):
      A_list[j] = (A_list[j] * factor) % mod
      factor = (factor * (j + 1)) % mod  
    c = step
    C = [1]
    for j in range(1, max_deg + 1):
      factor = (c * inv(j, mod)) % mod
      C.append((C[-1] * factor) % mod)
    D = convolution([A_list, C[::-1]])[max_deg:]
    factor = 1
    for i in range(len(D)):
      D[i] = (D[i] * factor) % mod
      factor = (factor * inv(i+1, mod)) % mod 
    return fps(D)
  
# example
A = [0, 1, 4]
B = [1, 3, 3, 1]
a = fps(A)
b = fps(B)
print(a + b, a - b)
print(a * b, a / b)
print(a // b, a % b)
print(a.differenciate())
print(b.integrate())
print(b.log())
print(a.exp())
print(a.power(2), b.power(1000))
print(b.shift(-1))

