from math import gcd
# 直線の係数が整数または小数の場合
# https://atcoder.jp/contests/jag2015summer-day4/submissions/37699281
def cht_append(a, b, cht_info): # 直線 y = a*x + b の追加(aは単調増加)
  # cht_info = [A分子, B分子, X分母, X分母]
  A_num, B_num, X_num, X_den = cht_info
  a_num = a #; a_den = 1;
  b_num = b #; b_den = 1;
  while X_num:
    ap_num, bp_num = A_num[-1], B_num[-1]
    x_num, x_den = X_num[-1], X_den[-1]
    if (ap_num - a_num) * x_num > (b_num - bp_num) * x_den: break
    A_num.pop()
    B_num.pop()
    X_num.pop()
    X_den.pop()
  if A_num:
    ap_num, bp_num = A_num[-1], B_num[-1]
    if ap_num == a_num:
      if bp_num >= b_num: return
      else: # ストックされた直線が一つしか残っておらず、これから追加する直線がそれと同じ傾きかつ大きい場合のみこのケース
        B_num[-1] = b_num
        return
    x_num, x_den = (b_num - bp_num), (ap_num - a_num)
    d = gcd(x_num, x_den)
    if x_den < 0: d *= -1
    X_num.append(x_num // d)
    X_den.append(x_den // d)
  A_num.append(a_num)
  B_num.append(b_num)  
  
def cht_value(x, cht_info): # 点xでの値を求める(xは整数)
  A_num, B_num, X_num, X_den = cht_info
  if not A_num: return None
  x_num = x
  lt = -1
  rt = len(X_num)
  while rt - lt > 1:
    ct = (rt + lt) // 2
    if x_num * X_den[ct] <= X_num[ct]:
      rt = ct
    else:
      lt = ct
  a_num_rt = A_num[rt]
  b_num_rt = B_num[rt]
  return a_num_rt * x_num + b_num_rt


from math import gcd
# 直線の係数として分数を許す場合
def cht_append(a, b, cht_info): # 直線 y = a*x + b の追加(aは単調増加)
  #　入力は a = [a分子, a分母], b = [b分子, b分母]
  # cht_info = [A分子, A分母, B分子, B分母, X分母, X分母]
  A_num, A_den, B_num, B_den, X_num, X_den = cht_info
  if isinstance(a, int):
    a_num = a; a_den = 1;
  else:
    a_num, a_den = a
    d = gcd(a_num, a_den)
    if a_den < 0: d *= -1
    a_num //= d; a_den //= d;
  b_num = b; b_den = 1;
  if isinstance(b, int):
    b_num = b; b_den = 1;
  else:
    b_num, b_den = b
    d = gcd(b_num, b_den)
    if b_den < 0: d *= -1
    b_num //= d; b_den //= d;
  while X_num:
    ap_num, bp_num = A_num[-1], B_num[-1]
    ap_den, bp_den = A_den[-1], B_den[-1]
    x_num, x_den = X_num[-1], X_den[-1]
    dna_num = ap_num * a_den - a_num * ap_den
    dna_den = ap_den * a_den
    db_num = b_num * bp_den - bp_num * b_den
    db_den = b_den * bp_den
    if dna_num * x_num * db_den > dna_den * x_den * db_num: break
    #if (ap - a) * x > (b - bp): break
    A_num.pop(); B_num.pop();
    A_den.pop(); B_den.pop();
    X_num.pop(); X_den.pop();
  if A_num:
    ap_num, bp_num = A_num[-1], B_num[-1]
    ap_den, bp_den = A_den[-1], B_den[-1]
    if ap_num * a_den == a_num * ap_den:
      if bp_num * b_den >= b_num * bp_den: return
      else: # ストックされた直線が一つしか残っておらず、これから追加する直線がそれと同じ傾きかつ大きい場合のみ
        B_num[-1] = b_num
        B_den[-1] = b_den
        return
    dna_num = ap_num * a_den - a_num * ap_den
    dna_den = ap_den * a_den
    db_num = b_num * bp_den - bp_num * b_den
    db_den = b_den * bp_den
    x_num = db_num * dna_den
    x_den = dna_num * db_den
    # x = (b - bp) / (ap - a)
    d = gcd(x_num, x_den)
    if x_den < 0: d *= -1
    X_num.append(x_num // d)
    X_den.append(x_den // d)
  A_num.append(a_num)
  A_den.append(a_den)
  B_num.append(b_num)  
  B_den.append(b_den)  
  
def cht_value(x, cht_info): # 点xでの値を求める(xは整数)
  #　入力は x = [x分子, x分母]
  # cht_info = [A分子, A分母, B分子, B分母, X分母, X分母]
  A_num, A_den, B_num, B_den, X_num, X_den = cht_info
  if not A_num: return None
  if isinstance(x, int):
    x_num = x; x_den = 1;
  else:
    x_num, x_den = x
    if x_den < 0:
      x_num *= -1; x_den *= -1;
  lt = -1
  rt = len(X_num)
  while rt - lt > 1:
    ct = (rt + lt) // 2
    if x_num * X_den[ct] <= x_den * X_num[ct]:
      rt = ct
    else:
      lt = ct
  a_num_rt = A_num[rt]
  a_den_rt = A_den[rt]
  b_num_rt = B_num[rt]
  b_den_rt = B_den[rt]
  c_num = a_num_rt * x_num
  c_den = a_den_rt * x_den
  return (c_num * b_den_rt + b_num_rt * c_den), (b_den_rt * c_den) # 出力: 分子, 分母
  # return a * x + b
  
