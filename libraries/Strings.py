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

# 30: Trie
class Trie():
  def __init__(self, words):
    self.I = [{}]
    self.words = []
    self.word_to_path = []
    for word in words:
      self.add_word(word)
      
  def add_word(self, word):  
    self.words.append(word)
    I = self.I
    word_to_path = self.word_to_path
    path = []
    now = 0
    for s in word:
      if s not in I[now]:
        I[now][s] = len(I)
        I.append({})
      now = I[now][s]
      path.append(now)
    word_to_path.append(path)

# 31: Aho_Corasick  
from collections import deque
class Aho_Corasick(Trie): # Trie木上でfailure込みのオートマトンを作る
  # self.words : 与えたwordのリスト(wordの番号はこの順につける)
  # self.I : その状態その文字でマッチした時の遷移先状態
  # self.failure : その状態でマッチしなかった時の遷移先状態
  # self.mark : その状態で直接ヒットしているwordの番号(1つと仮定)
  # self.mark_count : その状態におけるヒット数
  
  def __init__(self, words):
    super().__init__(words)
    self._mark_end()
    self._construct_failure()
    
  def __str__(self):
    ans = []
    ans.append("<< Aho-Corasick Trie >> \n")
    ans.append(" Word vs Path \n")
    for i, (path, word) in enumerate(zip(self.word_to_path, self.words)):
      ans.append("  " + word + " : " + str(path))
      ans.append("\n")
    ans.append(" Failure \n")
    ans.append("  " + str(self.failure))
    return "".join(ans)
    
  def _mark_end(self):
    word_to_path = self.word_to_path
    self.mark = mark = [None] * (len(self.I))
    for i, path in enumerate(word_to_path):
      mark[path[-1]] = i  
      
  def _construct_failure(self):
    I = self.I
    self.failure = failure = [None] * len(I)
    self.mark_count = mark_count = [0] * len(I)
    mark = self.mark
    
    task = deque([0])
    while task:
      p = task.popleft()
      for s, q in I[p].items():
        fp = failure[p]
        while fp is not None:
          if s in I[fp]:
            break
          else:
            fp = failure[fp]
        if fp is None:
          failure[q] = 0
        else:
          failure[q] = I[fp][s]
        mark_count[q] = mark_count[failure[q]] + int(mark[q] is not None)
        task.append(q)
        
  def relate_to(self, T):
    # Tの各文字をオートマトンの状態に対応付け
    now = 0
    ans = []
    I = self.I
    failure = self.failure
    for i, t in enumerate(T):
      while (now is not None) and (t not in I[now]):
        now = failure[now]
      if now is None:
        now = 0
      else:
        now = I[now][t]
      ans.append(now)
    return ans
    
  def count_match(self, T):
    mark_count = self.mark_count
    return sum([mark_count[a] for a in self.relate_to(T)])
    
  # 需要があれば
  #  各文字のヒットする箇所をすべて返す(計算量注意)
  #  各文字のヒットする最後の箇所を返す
