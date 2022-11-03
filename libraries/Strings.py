def Z_algorithm(S):
  # SとS[j:]の共通接頭辞長さを求める
  A = [0] * len(S)
 
  back = 1
  step = 0
  while len(S) > back:
    while len(S) > back + step and S[step] == S[back + step]: 
      step += 1
    A[back] = step
    
    if step == 0: 
      back += 1
      step = 0
      continue
    
    for dif in range(1, step+1):
      if dif == step or A[dif] >= step - dif: 
        back = back + dif
        step = step - dif
        break
      A[back + dif] = A[dif]
  
  A[0] = -1
  return A


def MP_algorithm(S):
  # S[:j]の接頭辞と接尾辞が一致するものの最長長さを求める（完全一致を除く）
  A = [0] * len(S)
  step = 0
  for now in range(1, len(S)):
    while step > 0 and S[now] != S[step]:
      step = A[step-1]
    if S[now] == S[step]:
      A[now] = step = step + 1
    else:
      A[now] = step = 0
      
  return A
