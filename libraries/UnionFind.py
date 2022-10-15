class UnionFind():
  def __init__(self, n):
    self.parent = [-1]*n # 親頂点（親頂点に対してはサイズの符号反転）
    self.rank = [0]*n # 深さ（の上限）
    
  def find(self, x): # xの親頂点
    par = self.parent
    if par[x] < 0:
      return x
    else:
      y = self.find(par[x])
      par[x] = y
      return y
    
  def same(self, x, y): # xとyが同じ連結成分に属すか判定
    find = self.find
    return find(x) == find(y)
  
  def merge(self, x, y): # xとyをマージする
    find = self.find
    x = find(x); y = find(y);
    if x == y: # もともと同じ成分なら何もしない
      return False
    rank = self.rank
    par = self.parent
    if rank[x] > rank[y]: # xが小さいほう、yが大きい方になるようにする
      x, y = y, x
    par[y] += par[x] # 頂点数
    par[x] = y # 親頂点の更新（結合）
    if rank[x] == rank[y]: # もとのランク（深さ）が同じ場合のみ、結合後の深さを1たす
      rank[y] += 1
    return True
  
  def size(self, x): # xを含む成分のサイズ
    return -self.parent[self.find(x)]
  
# 注意：加算以外の演算についてverifyされていない!!
class WeightedUnionFind():
  def __init__(self, n, op = lambda x, y: x + y, inv_op = lambda x: -x, ie = 0): # weightの演算と単位元を指定可能
    self.parent = [-1]*n # 親頂点（親頂点に対してはサイズの符号反転）
    self.rank = [0]*n # 深さ（の上限）
    self.op = op
    self.inv_op = inv_op
    self.ie = ie
    self.weight_dif = [ie]*n # 自分の直上の頂点との重みの差（自分 = op(親, dif)なるdif）
    
  def find(self, x): # xの最親頂点と、最親頂点との重みの差を返す（自分 = op(最親, dif)なるdif）
    par = self.parent
    op = self.op
    ie = self.ie
    weight_dif = self.weight_dif
    if par[x] < 0:
      return x, ie
    else:
      y, dw = self.find(par[x])
      dw = op(weight_dif[x], dw)
      par[x] = y
      weight_dif[x] = dw
      return y, dw
    
  def same(self, x, y): # xとyが同じ連結成分に属すか判定
    find = self.find
    return find(x)[0] == find(y)[0]
  
  def contradict(self, x, y, w): # op(weight[x], w) = weight[y] として矛盾するか判定
    find = self.find
    weight_dif = self.weight_dif
    op = self.op
    px, dwx = find(x); py, dwy = find(y);
    if px != py or dwy == op(dwx, w): return False # 矛盾なし
    else: return True
    
  def merge(self, x, y, w): # xとyをマージする。重みは、weight[y] = op(weight[x], w)となるようにする
    find = self.find
    weight_dif = self.weight_dif
    op = self.op
    inv_op = self.inv_op
    x, dwx = find(x); y, dwy = find(y);
    #print(dwx, w, dwy)
    w = op(op(dwx, w), inv_op(dwy))
    
    if x == y: # もともと同じ成分なら何もしない(注意：重みの値が矛盾する場合も、その旨応答しない)
      return False #何もしていないことを示すFalse
    
    rank = self.rank
    par = self.parent
    if rank[y] > rank[x]: # xが大きいほう、yが小さい方になるようにする
      x, y = y, x
      w = inv_op(w)
      
    par[x] += par[y] # 頂点数
    par[y] = x # 親頂点の更新（結合）
    weight_dif[y] = w
    if rank[x] == rank[y]: # もとのランク（深さ）が同じ場合のみ、結合後の深さを1ふやす
      rank[x] += 1
    return True
  
  def size(self, x): # xを含む成分のサイズ
    return -self.parent[self.find(x)]
