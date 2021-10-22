#include <bits/stdc++.h>
#include <atcoder/all>
using namespace std;
typedef long long int ll;
typedef long unsigned int ls_int;

# print list
void print(vector<ll> S){
  cout << "["; 
  for(ls_int i = 0; i < S.size(); i++){
    cout << S[i];
    if (i < S.size() - 1){
      cout << ", ";
    }
  }
  cout << "]" <<  endl;
}
void print(vector<int> S){
  cout << "["; 
  for(ls_int i = 0; i < S.size(); i++){
    cout << S[i];
    if (i < S.size() - 1){
      cout << ", ";
    }
  }
  cout << "]" <<  endl;
}
void print(vector<float> S){
  cout << "["; 
  for(ls_int i = 0; i < S.size(); i++){
    cout << S[i];
    if (i < S.size() - 1){
      cout << ", ";
    }
  }
  cout << "]" <<  endl;
}
void print(vector<string> S){
  cout << "["; 
  for(ls_int i = 0; i < S.size(); i++){
    cout << S[i];
    if (i < S.size() - 1){
      cout << ", ";
    }
  }
  cout << "]" <<  endl;
}

# sum of S[l, r)
int sum(vector<int> S, int l = 0, int r = -1){ /* sum of S[l, r) */
  int ans = 0;
  if (r == -1){
    r = S.size();
  }
  for (ls_int _ = ls_int(l); _ < ls_int(r); _++){
      ans += S[_];
  }
  return ans;
}
ll sum(vector<ll> S, int l = 0, int r = -1){ /* sum of S[l, r) */
  ll ans = 0;
  if (r == -1){
    r = S.size();
  }
  for (ls_int _ = ls_int(l); _ < ls_int(r); _++){
      ans += S[_];
  }
  return ans;
}
float sum(vector<float> S, int l = 0, int r = -1){ /* sum of S[l, r) */
  float ans = 0;
  if (r == -1){
    r = S.size();
  }
  for (ls_int _ = ls_int(l); _ < ls_int(r); _++){https://github.com/ken-svg/competitive_programming
      ans += S[_];
  }
  return ans;
}

# main function
int main(){
  
  
}
