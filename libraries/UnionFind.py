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
