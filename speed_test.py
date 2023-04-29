# test
N = 10 ** 5

from time import time

# 1. append
it = time()
for i in range(N):
  A.append(i)
print("append :", time() - it)
# append : 0.005374908447265625

it = time()
for i in range(N):
  A.append(i)
print("append_ret :", time() - it)
# append_ret : 0.005942821502685547


# 2. pop
it = time()
for i in range(N):
  A.append(i)
print("pop  :", time() - it)
# pop  : 0.0048313140869140625


# 3. insert
A = [a for a in range(N)]
it = time()
A.append(A[-1])
for i in range(N-1, -1, -1):
  A[i] = A[i-1]
A[0] = 1
print("insert_top_manual :", time() - it)
# insert_top_manual : 0.0015807151794433594

A = [a for a in range(N)]
it = time()
A.insert(0, 1) 
print("insert_top :", time() - it)
# insert_top : 3.9577484130859375e-05

A = [a for a in range(N)]
it = time()
A.insert(-1, 1) 
print("insert_tail :", time() - it)
# insert_tail : 5.245208740234375e-06

A = [a for a in range(N)]
it = time()
A.insert(N//2, 1) 
print("insert_middle :", time() - it)
# insert_middle : 1.7404556274414062e-05


# 4. find
A = [a for a in range(N)]
to_be_found = N-1
it = time()
for i, a in enumerate(A):
  if a == to_be_found:
    j = i
    break
print("find_manual :", time() - it)
# find_manual : 0.0010254383087158203

A = [a for a in range(N)]
to_be_found = N-1
it = time()
j = A.index(to_be_found)
print("find :", time() - it) 
# find : 7.224082946777344e-05


# 5. max, min
A = [a for a in range(N)]
it = time()
val = -1
for a in A:
  if val < a:
    val = a
print("max_manual :", time() - it) 
# max_manual : 0.001008749008178711

A = [a for a in range(N)]
it = time()
val = max(A)
print("max :", time() - it) 
# max : 0.0004775524139404297

# 6. sum
A = [a for a in range(N)]
it = time()
val = 0
for a in A:
  val += a
print("sum_manual :", time() - it) 
# sum_manual : 0.0009229183197021484

A = [a for a in range(N)]
it = time()
val = sum(A)
print("sum :", time() - it) 
# sum : 0.000637054443359375


# 7. remove
A = [a for a in range(N)]
to_be_found = N // 2
it = time()
for i, a in enumerate(A):
  if a == to_be_found:
    A = A[:i] + A[i+1:]
  break
print("remove_manual :", time() - it)  
# remove_manual : 9.298324584960938e-06

A = [a for a in range(N)]
to_be_found = N // 2
it = time()
A.remove(to_be_found)
print("remove :", time() - it) 
# remove : 7.176399230957031e-05


# 8. extend
A = [a for a in range(N)]
B = [a for a in range(N)]
it = time()
for b in B:
  A.append(b)
print("extend_manual:", time() - it) 
# extend_manual: 0.0026226043701171875

A = [a for a in range(N)]
B = [a for a in range(N)]
it = time()
A += B
print("extend_plus:", time() - it) 
# extend_plus: 0.0002598762512207031

A = [a for a in range(N)]
B = [a for a in range(N)]
it = time()
A.extend(B)
print("extend:", time() - it)  
# extend: 0.0002799034118652344


# 9. count
A = [a % 10 for a in range(N)]
to_be_found = 2
it = time()
ct = 0
for a in A:
  if a == to_be_found:
    ct += 1
print("count_manual:", time() - it) 
# count_manual: 0.0015423297882080078

A = [a % 10 for a in range(N)]
to_be_found = 2
it = time()
ct = A.count(to_be_found)
print("count:", time() - it) 
# count: 0.0034728050231933594


# 10. copy
A = [a for a in range(N)]
it = time()
B = [a for a in A]
print("copy_manual:", time() - it) 
# copy_manual: 0.0018315315246582031

A = [a for a in range(N)]
it = time()
B = A.copy()
print("copy:", time() - it) 
# copy: 0.00042700767517089844


# 11. reverse
A = [a for a in range(N)]
it = time()
A = [A[i] for i in range(len(A)-1, -1, -1)]
print("reverse_manual:", time() - it)
# reverse_manual: 0.002355337142944336

A = [a for a in range(N)]
it = time()
A = A[::-1]
print("reverse_slice:", time() - it)
# reverse_slice: 0.00019025802612304688

A = [a for a in range(N)]
it = time()
A.reverse()
print("reverse:", time() - it)
# reverse: 4.3392181396484375e-05


# 11.access
A = [a for a in range(N)]
J = list(range(N))
it = time()
for i in J:
  b = A[i]
print("access:", time() - it)
# access: 0.0010287761688232422

A = [a for a in range(N)]
J = list(range(N-1, -1, -1))
it = time()
for i in J:
  b = A[i]
print("access_reverse:", time() - it)
# access_reverse: 0.001035928726196289

from random import randint
J = [randint(0, N-1) for _ in range(N)]
A = [a for a in range(N)]
it = time()
for i in J:
  b = A[i]
print("access_random:", time() - it)  
# access_random: 0.001218557357788086

A = [a for a in range(N)]
it = time()
for a in A:
  b = a
print("access_inclusive:", time() - it)  
# access_inclusive: 0.0008406639099121094


# 12. strinig_concat
A = ["a"] * N
it = time()
v = ""
for a in A:
  v += a
print("strinig_concat_plus:", time() - it) 
# strinig_concat_plus: 0.3863840103149414

A = ["a"] * N
it = time()
v = "".join(A)
print("strinig_concat_join:", time() - it) 
# strinig_concat_join: 0.0006356239318847656

