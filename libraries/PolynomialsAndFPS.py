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
  
def polynomial_taylor_shift(A, d): # A(x) -> A(x+d)
  N = len(A) - 1
  fact = [1]
  tmp = 1
  for i in range(1, N+1):
    tmp *= i
    tmp %= mod
    fact.append(tmp)
  V = [(A[i] * fact[i]) % mod for i in range(N, -1, -1)]
  W = [1]
  tmp = 1
  for i in range(1, N+1):
    tmp *= inv(i, mod)
    tmp %= mod
    tmp *= d
    tmp %= mod
    W.append(tmp)
  B = fps_power(V, W)[N::-1]
  tmp = 1
  for i in range(N+1):
    B[i] = (B[i] * tmp) % mod
    tmp *= inv(i+1, mod)
    tmp %= mod
  return B

def Bostan_Mori(P, Q, N): # [x^N] P(x) / Q(x)
  num = P[:N+1]
  den = Q[:N+1]
  while N >= 1:
    den_neg = []
    fac = 1
    for q in den:
      den_neg.append(q * fac)
      fac *= -1
    num = fps_power(num, den_neg)[N%2:N+1:2]
    den = fps_power(den, den_neg)[0:N+1:2]

    N //= 2
  
  return num[0] * inv(den[0], mod)

def fps_commonize_denominator(P, Q): # P[i]/Q[i] の和を通分
  def derive(l, r, P, Q):
    if r - l == 1:
      return [P[l], Q[l]]
    c = (r + l) // 2
    Pl, Ql = derive(l, c, P, Q)
    Pr, Qr = derive(c, r, P, Q)
    P1 = fps_power(Ql, Pr)
    P2 = fps_power(Qr, Pl)
    Q = fps_power(Ql, Qr)
    while P1[-1] == 0: P1.pop()
    while P2[-1] == 0: P2.pop()
    while Q[-1] == 0: Q.pop()
    if len(P1) > len(P2):
      P1, P2 = P2, P1
    for i, p in enumerate(P1):
      P2[i] += p
      P2[i] %= mod
    return P2, Q
  return derive(0, len(P), P, Q)



  
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

