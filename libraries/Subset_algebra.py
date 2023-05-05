def Subset_Zeta_conversion(A, inplace = True, op = lambda a0, a1: (a0 + a1) % (998244353)):
  if not inplace:
    A = [a for a in A]
  A_len = len(A)
  N = A_len.bit_length() - 1
  
  for n in range(N):
    for i in range(A_len):
      if i & (1 << n):
        A[i] = op(A[i ^ (1 << n)], A[i])    
  return A

def Subset_Mobius_conversion(A, inplace = True, inv_op = lambda a0, a1: (a1 - a0) % (998244353)):
  if not inplace:
    A = [a for a in A]
  A_len = len(A)
  N = A_len.bit_length() - 1
  
  for n in range(N):
    for i in range(A_len):
      if i & (1 << n):
        A[i] = inv_op(A[i ^ (1 << n)], A[i])    
  return A

def Subset_Bitwise_OR_convolution(A, B, inplace = True, op = lambda a0, a1: (a0 + a1) % (998244353), inv_op = lambda a0, a1: (a1 - a0) % (998244353), conv_prod = lambda x, y: (x * y) % (998244353)):
  # require Subset_Zeta_conversion, Subset_Mobius_conversion
  A_len = len(A)
  N = A_len.bit_length() - 1
  
  ZA = Subset_Zeta_conversion(A, inplace = inplace, op = op)
  ZB = Subset_Zeta_conversion(B, inplace = inplace, op = op)
  ZC = [conv_prod(za, zb) for za, zb in zip(ZA, ZB)]
  C = Subset_Mobius_conversion(ZC, inplace = True, inv_op = inv_op)
  return C

mod = 998244353
def Subset_Convolution(A, B, inplace = True, add_op = lambda x, y: (x + y) % mod, inv_add_op = lambda x, y: (y - x) % mod, prod_op = lambda x, y: (x * y) % mod):
  A_len = len(A)
  N = A_len.bit_length() - 1
  
  pop_count = [0] * A_len
  for i in range(N):
    pop_count[1 << i] += 1
  pop_count = Subset_Zeta_conversion(pop_count)
  
  A_degfied = [[0 if j != pop_count[i] else a for j in range(N + 1)] for i, a in enumerate(A)]
  B_degfied = [[0 if j != pop_count[i] else a for j in range(N + 1)] for i, a in enumerate(B)]
  def add_degfied(a0, a1):
    return [add_op(v0, v1) for v0, v1 in zip(a0, a1)]
  def inv_add_degfied(a0, a1):
    return [inv_add_op(v0, v1) for v0, v1 in zip(a0, a1)]
  def prod_degfied(a0, a1):
    v = [0] * (len(a0) + len(a1) - 1)
    for i0, v0 in enumerate(a0):
      for i1, v1 in enumerate(a1):
        v[i0 + i1] = add_op(v[i0 + i1], prod_op(v0, v1))
    return v
  
  SBOC = Subset_Bitwise_OR_convolution(A_degfied, B_degfied, inplace = inplace, op = add_degfied, inv_op = inv_add_degfied, conv_prod = prod_degfied)
  S = [v[pop_count[i]] for i, v in enumerate(SBOC)]
  
  return S


"""
N = 17
from random import randint
A = [randint(1, 10 ** 9) for i in range(1 << N)]
B = [randint(1, 10 ** 9) for i in range(1 << N)]

VA = A.copy()
VB = B.copy()

from time import time
it = time()
Q = Subset_Convolution(A, B)
print(time() - it)
#2.90 sec
"""

def Subset_Convolution_for_normal_prod(A, B):
  # 通常の和積限定で定数倍を（ほんの少し）改善した
  A_len = len(A)
  N = A_len.bit_length() - 1
  
  pop_count = [0] * A_len
  for i in range(N):
    pop_count[1 << i] += 1
  for i in range(N):
    for j in range(1 << N):
      if j & (1 << i):
        pop_count[j] += pop_count[j ^ (1 << i)]
  
  A_degfied = [[0 if j != pop_count[i] else a for j in range(N + 1)] for i, a in enumerate(A)]
  B_degfied = [[0 if j != pop_count[i] else a for j in range(N + 1)] for i, a in enumerate(B)]
  
  for degfied in [A_degfied, B_degfied]:
    for i in range(N):
      for j in range(1 << N):
        if j & (1 << i):
          degfied_0 = degfied[j ^ (1 << i)]
          degfied_1 = degfied[j]
          for l in range(N+1):
            degfied_1[l] += degfied_0[l]
  
  C = []
  for j, (A_degfied_j, B_degfied_j) in enumerate(zip(A_degfied, B_degfied)):
    pop_j = pop_count[j]
    
    val = [0] * (N + 1 - pop_j)
    for k in range(N + 1):
      A_degfied_j_k = A_degfied_j[k]
      for l in range(max(0, pop_j - k), N - k + 1):
        val[k + l - pop_j] += A_degfied_j_k * B_degfied_j[l]
      if mod:
        val[k + l - pop_j] %= mod
    C.append(val)
  
  for i in range(N):
    for j, C_1 in enumerate(C):
      if j & (1 << i):
        j0 = j ^ (1 << i)
        C_0 = C[j0]
        pop_ct_0 = pop_count[j0]
        pop_ct_1 = pop_count[j]
        #C_1 = C[j]
        for l in range(pop_count[j], N+1):
          C_1[l - pop_ct_1] -= C_0[l - pop_ct_0]
  
  C = [v[0] for j, v in enumerate(C)]
  if mod:
    C = [c % mod for c in C]
  return C

"""
it = time()
R = Subset_Convolution_for_normal_prod(VA, VB)
print(time() - it)
#2.60 sec
print(Q == R)
"""


        
    
