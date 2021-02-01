# https://atcoder.jp/contests/abc141/submissions/19868144

import random
N = int(input())
S = input()
S = [ord(s) for s in S]

def main(mod):
  base = random.randint(200,10000)

  hash_sum = [0]
  for s in S:
    hash_sum.append((hash_sum[-1] * base + s) % mod
    
  pow_base = [1]
  for _ in range(N):
    pow_base.append((pow_base[-1]*base) % mod)
    
  for l in range(N//2,-1,-1):
    flag = False
    vis = set()
    for i in range(N-2*l+1):
      hash_l = hash_sum[i+l] - hash_sum[i] * pow_base[l] # S[i:i+l]のhash
      hash_l %= mod
      hash_r = hash_sum[i+2*l] - hash_sum[i+l] * pow_base[l] # S[i+l:i+2*l]のhash
      hash_r %= mod
      #print(hash_l, S[i:i+l])
      vis.add(hash_l)

      if hash_r in vis: 
        return l
      
mods = [6158965020334]
ans = 0
for mod in mods:
  ans = max(ans, main(mod))
print(ans)
