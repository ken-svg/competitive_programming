def Zalgorithm(S):
  # S と S[i:|S|-1] の最長共通接頭辞の長さを求める
  N = len(S)
  i = 1
  j = 0
  ans = [0] * N
  ans[0] = N
  while i < N:
    while i + j < N and S[i+j] == S[j]:
      j += 1
    ans[i] = j
    sft = 1
    while i + sft < N and ans[sft] < j - sft:
      ans[i+sft] = ans[sft]
      sft += 1
    i += sft
    j = max(0, j - sft)
  
  return ans
