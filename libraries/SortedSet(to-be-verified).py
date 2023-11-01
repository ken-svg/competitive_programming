from math import sqrt, ceil, floor
from bisect import bisect_left, bisect_right
class SortedSet():
  def __init__(self, data):
    self.BACKET_RATIO_INIT = 40
    self.BACKET_RATIO_MAX = 120 # 2 * self.BACKET_RATIO_INIT より大きく
    self.sum_activated = False
    
    data = list(set(data)) #MultiSetの場合はこの処理いらない
    data.sort()
    self.length = len(data)
    if self.length > 0:
      self.A = [data]
      self._const() 
    else:
      self.A = []
  
  def _const(self):
    if self.length == 0:
      self.A = []
      return
    backet_num = max(1, floor(sqrt(self.length / self.BACKET_RATIO_INIT)))
    A_list = []
    length = self.length
    for a in self.A:
      A_list.extend(a)
    self.A = [A_list[length * i // backet_num : length * (i+1) // backet_num] for i in range(backet_num)]
    if self.sum_activated:
      self.A_sum = [sum(a) for a in self.A]
    return 
    
  def __len__(self):
    return self.length
  
  def __contains__(self, x):
    if self.length == 0: return False
    target = None
    for a in self.A:
      if x <= a[-1]:
        target = a
        break
    if target is not None:
      j = bisect_left(target, x)
      if j < len(target) and target[j] == x: return True
    return False
  
  def sum_activate(self):
    self.sum_activated = True
    self.A_sum = [sum(a) for a in self.A]
  
  def add(self, x):
    if self.length == 0:
      self.A = [[x]]
      if self.sum_activated:
        self.A_sum = [x]
      self.length = 1
      return True
    
    target = None
    for i, a in enumerate(self.A):
      if x <= a[-1]:
        target = a
        break
    if target is None:
      target = self.A[-1]
    j = bisect_left(target, x)
    if j < len(target) and target[j] == x: #MultiSetの場合はこの処理いらない
      return False
    else:
      target.insert(j, x)
      self.length += 1
      if self.sum_activated:
        self.A_sum[i] += x
      if len(target) > len(self.A) * self.BACKET_RATIO_MAX:
        self._const()
      return True
  
  def remove(self, x):
    if self.length == 0: return False
    target = None
    for i, a in enumerate(self.A):
      if x <= a[-1]:
        target = a
        break
    if target is None: return False
    j = bisect_left(target, x)
    if j < len(target) and target[j] == x: 
      target.pop(j)
      self.length -= 1
      if self.sum_activated:
        self.A_sum[i] -= x
      if not target and self.length > 0:
        self._const()
      return True
    else:
      return False
    
  def __getitem__(self, i):
    if i < 0:
      i += self.length
    if not(0 <= i < self.length):
      raise IndexError
    now = 0
    target = None
    for a in self.A:
      if now + len(a) > i:
        target = a
        break
      now += len(a)
    return target[i - now]
        
    
  def lt(self, x):
    if self.length == 0: return None
    target = None
    for a in self.A:
      if a[0] < x:
        target = a
      else: break
    if target is None: return None
    j = bisect_left(target, x)
    return target[j-1]
  
  def le(self, x):
    if self.length == 0: return None
    target = None
    for a in self.A:
      if a[0] <= x:
        target = a
      else: break
    if target is None: return None
    j = bisect_right(target, x)
    return target[j-1]
    
  def rt(self, x):
    if self.length == 0: return None
    target = None
    for a in self.A:
      if x < a[-1]:
        target = a
        break
    if target is None: return None
    j = bisect_right(target, x)
    return target[j]
  
  def re(self, x):
    if self.length == 0: return None
    target = None
    for a in self.A:
      if x <= a[-1]:
        target = a
        break
    if target is None: return None
    j = bisect_left(target, x)
    return target[j]
    
  def lt_count(self, x): # <x の個数
    if self.length == 0: return 0
    ans = 0
    target = None
    for a in self.A:
      if a[0] < x:
        target = a
        ans += len(target)
      else: break
    if target is None: return 0
    j = bisect_left(target, x)
    ans += -len(target) + j
    return ans
  
  def le_count(self, x): # <=x の個数
    if self.length == 0: return 0
    ans = 0
    target = None
    for a in self.A:
      if a[0] <= x:
        target = a
        ans += len(target)
      else: break
    if target is None: return 0
    j = bisect_right(target, x)
    ans += -len(target) + j
    return ans
  
  def rt_count(self, x): # x< の個数
    if self.length == 0: return 0
    ans = self.length
    target = None
    for a in self.A:
      ans -= len(a)
      if x < a[-1]:
        ans += len(a)
        target = a
        break
    if target is None: return 0
    j = bisect_right(target, x)
    ans -= j
    return ans
  
  def re_count(self, x): # x<= の個数
    if self.length == 0: return 0
    ans = self.length
    target = None
    for a in self.A:
      ans -= len(a)
      if x <= a[-1]:
        ans += len(a)
        target = a
        break
    if target is None: return 0
    j = bisect_left(target, x)
    ans -= j
    return ans
  
  def lt_sum(self, x): # <x の総和
    if not self.sum_activated: return False
    if self.length == 0: return 0
    ans = 0
    target = None
    for a, s in zip(self.A, self.A_sum):
      if a[0] < x:
        target = a
        ans += s
      else: break
    if target is None: return 0
    j = bisect_left(target, x)
    ans += -s + sum(target[:j])
    return ans
  
  def le_sum(self, x): # <=x の総和
    if not self.sum_activated: return False
    if self.length == 0: return 0
    ans = 0
    target = None
    for a, s in zip(self.A, self.A_sum):
      if a[0] <= x:
        target = a
        ans += s
      else: break
    if target is None: return 0
    j = bisect_right(target, x)
    ans += -s + sum(target[:j])
    return ans
    
  def rt_sum(self, x): # x< の総和
    if not self.sum_activated: return False
    if self.length == 0: return 0
    ans = sum(self.A_sum)
    target = None
    for a, s in zip(self.A, self.A_sum):
      ans -= s
      if x < a[-1]:
        ans += s
        target = a
        break
    if target is None: return 0
    j = bisect_right(target, x)
    ans -= sum(target[:j])
    return ans
  
  def re_sum(self, x): # x<= の総和
    if not self.sum_activated: return False
    if self.length == 0: return 0
    ans = sum(self.A_sum)
    target = None
    for a, s in zip(self.A, self.A_sum):
      ans -= s
      if x <= a[-1]:
        ans += s
        target = a
        break
    if target is None: return 0
    j = bisect_left(target, x)
    ans -= sum(target[:j])
    return ans
  
  def left_index_sum(self, i):
    if not self.sum_activated: return False
    if not(0 <= i < self.length):
      raise IndexError
    now = 0
    ans = 0
    target = None
    for a, s in zip(self.A, self.A_sum):
      if now + len(a) > i:
        target = a
        break
      now += len(a)
      ans += s
    ans += sum(target[:i-now+1])
    return ans
  
  def right_index_sum(self, i):
    if not self.sum_activated: return False
    if not(0 <= i < self.length):
      raise IndexError
    now = 0
    ans = 0
    target = None
    for a, s in zip(reversed(self.A), reversed(self.A_sum)):
      if now + len(a) > i:
        target = a
        break
      now += len(a)
      ans += s
    ans += sum(target[-(i-now)-1:])
    return ans
  
  def __str__(self):
    ans = ["{"]
    for a in self.A:
      for v in a:
        ans.append(str(v))
        ans.append(", ")
    ans.pop()
    ans.append("}")
    return "".join(ans)



from math import sqrt, ceil, floor
from bisect import bisect_left, bisect_right
class SortedMultiSet():
  def __init__(self, data):
    self.BACKET_RATIO_INIT = 40
    self.BACKET_RATIO_MAX = 120 # 2 * self.BACKET_RATIO_INIT より大きく
    self.sum_activated = False
    
    #data = list(set(data)) #MultiSetの場合はこの処理いらない
    data.sort()
    self.length = len(data)
    if self.length > 0:
      self.A = [data]
      self._const() 
    else:
      self.A = []
  
  def _const(self):
    if self.length == 0:
      self.A = []
      return
    backet_num = max(1, floor(sqrt(self.length / self.BACKET_RATIO_INIT)))
    A_list = []
    length = self.length
    for a in self.A:
      A_list.extend(a)
    self.A = [A_list[length * i // backet_num : length * (i+1) // backet_num] for i in range(backet_num)]
    if self.sum_activated:
      self.A_sum = [sum(a) for a in self.A]
    return 
    
  def __len__(self):
    return self.length
  
  def __contains__(self, x):
    if self.length == 0: return False
    target = None
    for a in self.A:
      if x <= a[-1]:
        target = a
        break
    if target is not None:
      j = bisect_left(target, x)
      if j < len(target) and target[j] == x: return True
    return False
  
  def sum_activate(self):
    self.sum_activated = True
    self.A_sum = [sum(a) for a in self.A]
  
  def add(self, x):
    if self.length == 0:
      self.A = [[x]]
      if self.sum_activated:
        self.A_sum = [x]
      self.length = 1
      return True
    
    target = None
    for i, a in enumerate(self.A):
      if x <= a[-1]:
        target = a
        break
    if target is None:
      target = self.A[-1]
    j = bisect_left(target, x)
    if False: #MultiSetの場合はこの処理いらない
      return False
    else:
      target.insert(j, x)
      self.length += 1
      if self.sum_activated:
        self.A_sum[i] += x
      if len(target) > len(self.A) * self.BACKET_RATIO_MAX:
        self._const()
      return True
  
  def remove(self, x):
    if self.length == 0: return False
    target = None
    for i, a in enumerate(self.A):
      if x <= a[-1]:
        target = a
        break
    if target is None: return False
    j = bisect_left(target, x)
    if j < len(target) and target[j] == x: 
      target.pop(j)
      self.length -= 1
      if self.sum_activated:
        self.A_sum[i] -= x
      if not target and self.length > 0:
        self._const()
      return True
    else:
      return False
    
  def __getitem__(self, i):
    if i < 0:
      i += self.length
    if not(0 <= i < self.length):
      raise IndexError
    now = 0
    target = None
    for a in self.A:
      if now + len(a) > i:
        target = a
        break
      now += len(a)
    return target[i - now]
        
    
  def lt(self, x):
    if self.length == 0: return None
    target = None
    for a in self.A:
      if a[0] < x:
        target = a
      else: break
    if target is None: return None
    j = bisect_left(target, x)
    return target[j-1]
  
  def le(self, x):
    if self.length == 0: return None
    target = None
    for a in self.A:
      if a[0] <= x:
        target = a
      else: break
    if target is None: return None
    j = bisect_right(target, x)
    return target[j-1]
    
  def rt(self, x):
    if self.length == 0: return None
    target = None
    for a in self.A:
      if x < a[-1]:
        target = a
        break
    if target is None: return None
    j = bisect_right(target, x)
    return target[j]
  
  def re(self, x):
    if self.length == 0: return None
    target = None
    for a in self.A:
      if x <= a[-1]:
        target = a
        break
    if target is None: return None
    j = bisect_left(target, x)
    return target[j]
    
  def lt_count(self, x): # <x の個数
    if self.length == 0: return 0
    ans = 0
    target = None
    for a in self.A:
      if a[0] < x:
        target = a
        ans += len(target)
      else: break
    if target is None: return 0
    j = bisect_left(target, x)
    ans += -len(target) + j
    return ans
  
  def le_count(self, x): # <=x の個数
    if self.length == 0: return 0
    ans = 0
    target = None
    for a in self.A:
      if a[0] <= x:
        target = a
        ans += len(target)
      else: break
    if target is None: return 0
    j = bisect_right(target, x)
    ans += -len(target) + j
    return ans
  
  def rt_count(self, x): # x< の個数
    if self.length == 0: return 0
    ans = self.length
    target = None
    for a in self.A:
      ans -= len(a)
      if x < a[-1]:
        ans += len(a)
        target = a
        break
    if target is None: return 0
    j = bisect_right(target, x)
    ans -= j
    return ans
  
  def re_count(self, x): # x<= の個数
    if self.length == 0: return 0
    ans = self.length
    target = None
    for a in self.A:
      ans -= len(a)
      if x <= a[-1]:
        ans += len(a)
        target = a
        break
    if target is None: return 0
    j = bisect_left(target, x)
    ans -= j
    return ans
  
  def lt_sum(self, x): # <x の総和
    if not self.sum_activated: return False
    if self.length == 0: return 0
    ans = 0
    target = None
    for a, s in zip(self.A, self.A_sum):
      if a[0] < x:
        target = a
        ans += s
      else: break
    if target is None: return 0
    j = bisect_left(target, x)
    ans += -s + sum(target[:j])
    return ans
  
  def le_sum(self, x): # <=x の総和
    if not self.sum_activated: return False
    if self.length == 0: return 0
    ans = 0
    target = None
    for a, s in zip(self.A, self.A_sum):
      if a[0] <= x:
        target = a
        ans += s
      else: break
    if target is None: return 0
    j = bisect_right(target, x)
    ans += -s + sum(target[:j])
    return ans
    
  def rt_sum(self, x): # x< の総和
    if not self.sum_activated: return False
    if self.length == 0: return 0
    ans = sum(self.A_sum)
    target = None
    for a, s in zip(self.A, self.A_sum):
      ans -= s
      if x < a[-1]:
        ans += s
        target = a
        break
    if target is None: return 0
    j = bisect_right(target, x)
    ans -= sum(target[:j])
    return ans
  
  def re_sum(self, x): # x<= の総和
    if not self.sum_activated: return False
    if self.length == 0: return 0
    ans = sum(self.A_sum)
    target = None
    for a, s in zip(self.A, self.A_sum):
      ans -= s
      if x <= a[-1]:
        ans += s
        target = a
        break
    if target is None: return 0
    j = bisect_left(target, x)
    ans -= sum(target[:j])
    return ans
  
  def left_index_sum(self, i):
    if not self.sum_activated: return False
    if not(0 <= i < self.length):
      raise IndexError
    now = 0
    ans = 0
    target = None
    for a, s in zip(self.A, self.A_sum):
      if now + len(a) > i:
        target = a
        break
      now += len(a)
      ans += s
    ans += sum(target[:i-now+1])
    return ans
  
  def right_index_sum(self, i):
    if not self.sum_activated: return False
    if not(0 <= i < self.length):
      raise IndexError
    now = 0
    ans = 0
    target = None
    for a, s in zip(reversed(self.A), reversed(self.A_sum)):
      if now + len(a) > i:
        target = a
        break
      now += len(a)
      ans += s
    ans += sum(target[-(i-now)-1:])
    return ans
  
  def __str__(self):
    ans = ["{"]
    for a in self.A:
      for v in a:
        ans.append(str(v))
        ans.append(", ")
    ans.pop()
    ans.append("}")
    return "".join(ans)
