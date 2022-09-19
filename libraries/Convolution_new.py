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
