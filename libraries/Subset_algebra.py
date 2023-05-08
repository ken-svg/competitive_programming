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
def Subset_Convolution_for_general(A, B, add_op = lambda x, y: (x + y) % (998244353),
                                   inv_add_op = lambda x, y: (y - x) % (998244353),
                                   add_identity = 0,
                                   prod_op = lambda x, y: (x * y) % (998244353)):
  A_len = len(A)
  N = A_len.bit_length() - 1
  
  pop_count = [0] * A_len
  for i in range(N):
    pop_count[1 << i] += 1
  for i in range(N):
    for j in range(1 << N):
      if j & (1 << i):
        pop_count[j] += pop_count[j ^ (1 << i)]
  
  A_degfied = [[add_identity] * p + [a] for a, p in zip(A, pop_count)]
  B_degfied = [[add_identity] * p + [a] for a, p in zip(B, pop_count)]
  
  for degfied in [A_degfied, B_degfied]:
    for i in range(N):
      for j_h in range(1 << i, len(A), 1 << (i + 1)):
        for j_l in range(1 << i):
          j = j_h | j_l
          degfied_0 = degfied[j ^ (1 << i)]
          degfied_1 = degfied[j]
          pop_ct_j = pop_count[j]
          for l in range(pop_ct_j):
            degfied_1[l] = add_op(degfied_0[l], degfied_1[l])
  
  C = []
  for j, (A_degfied_j, B_degfied_j) in enumerate(zip(A_degfied, B_degfied)):
    pop_j = pop_count[j]
    
    val = []
    for x in range(pop_j, N + 1):
      # k + l = x
      # 0 <= k <= pop_j, 0 <= l <= pop_j
      tmp = add_identity
      for k in range(max(x - pop_j, 0), min(pop_j, x) + 1):
        l = x - k
        tmp = add_op(tmp, prod_op(A_degfied_j[k], B_degfied_j[l]))
      val.append(tmp)
    C.append(val)
  
  for i in range(N):
    for j_h in range(1 << i, len(C), 1 << (i + 1)):
      for j_l in range(1 << i):
        j = j_h | j_l
        j0 = j ^ (1 << i)
        C_0 = C[j0]
        C_1 = C[j]
        
        pop_ct_1 = pop_count[j]
        pop_ct_0 = pop_ct_1 - 1
        for l in range(pop_ct_1, min(pop_ct_1 + N-1-i, N)+1):
          C_1[l - pop_ct_1] = inv_add_op(C_0[l - pop_ct_0], C_1[l - pop_ct_1])
  
  C = [v[0] for v in C]
  return C

        
    
