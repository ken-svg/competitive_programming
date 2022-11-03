# 10: Z_algorithm
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

# 20: MP_algorithm(prefix_function)
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

# 20_1: _return_table (-> KMP_search)
def _return_table(MPS, S):
  # MPS(Sのprefix function)とSからKMPで使用する部分マッチテーブルを作成
  W = [MPS[i]-1 for i in range(len(S))]
  for i in range(1, len(S)-1):
    s = S[i+1]
    j = i
    while j >= 0 and s == S[j+1]:
      j = W[j]
    W[i] = j
  return W

# 21: KMP_search
def KMP_search(A, B, complete_search = False):
  # 文字列AからBをサーチする
  # MP_algorithmと_return_tableを必要とする
  if len(A) < len(B):
    return [] if complete_search else -1
  
  RTB = _return_table(MP_algorithm(B), B)
  
  if complete_search:
    ans = [] 
  state = -1
  for i in range(len(A)):
    while state >= 0 and A[i] != B[state + 1]:
      state = RTB[state]
    if A[i] != B[state + 1]:
      continue
      
    state += 1
    if state == len(B) - 1:
      if complete_search:
        ans.append(i - len(B) + 1)
        state = RTB[state]
      else:
        return i - len(B) + 1
    
  return ans
