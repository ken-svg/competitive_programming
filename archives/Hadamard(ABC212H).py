# 提出例：https://atcoder.jp/contests/abc212/submissions/24714375

# 逆元
mod = 998244353
# mod = 素数
_inv_t = {}
_inv_t[1] = 1
_inv_t[0] = 0
def inv(x, mod):
  x %= mod
  if x not in _inv_t:
    _inv_t[x] = inv(mod % x, mod) * (mod - mod // x) % mod
  return _inv_t[x]

N, K = map(int,input().split())
A = list(map(int,input().split()))
S = max(A)
L = 1 << S.bit_length()

V = [0 for _ in range(L)]
for a in A:
  #print(a, L)
  V[a] += 1
  
# アダマール変換
sft = 0
for _ in range((len(V)-1).bit_length()):
  V_next = []
  for s in range(len(V)):
    if 1 & (s >> sft):
      s0 = s ^ (1 << sft)
      s1 = s
      V_next.append((V[s0] - V[s1]) % mod)
    else:
      s1 = s ^ (1 << sft)
      s0 = s
      V_next.append((V[s0] + V[s1]) % mod)
  sft += 1
  
  V = V_next
  #print(V)
  
  
ans = 0
L_inv = inv(L, mod)
for v in V:
  #r = (v * inv(N, mod)) % mod
  r = v
  if r == 1:
    ans += N
    ans %= mod
  else:
    ans += (r * (1-pow(r,N,mod)) % mod) * inv(1-r, mod)
    ans %= mod
  
ans *= L_inv
ans %= mod
#print(ans)

ans = ((K * (1 - pow(K,N,mod)) * inv(1-K, mod)) if K % mod != 1 else N) - ans
print(ans % mod)
  
