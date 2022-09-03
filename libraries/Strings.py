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


def prefix_function(S): # S[0:i]の接尾辞と接頭辞の一致数のうち、非自明なものの最大
  N = len(S)
  i, j = 1, 0
  prefix = [0] * N
  for i in range(1, N):
    while j > 0 and S[i] != S[j]:
      j = prefix[j-1]
    if S[i] == S[j]:
      j += 1
    prefix[i] = j
  return prefix
