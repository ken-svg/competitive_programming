#include <bits/stdc++.h>
#include <atcoder/all>
using namespace std;
typedef long long int ll;
typedef long unsigned int ls_int;
#define heapq priority_queue

// 1-1, print list
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


// 1-2, print matrix
void print(vector<vector<int>> S){
  cout << "["; 
  for(ls_int i = 0; i < S.size(); i++){
    cout << "["; 
    for(ls_int j = 0; j < S.at(i).size(); j++){
      cout << S.at(i).at(j);
      if (j < S.at(i).size() - 1){
        cout << ", ";
      } 
    }
    cout << "]";
    if (i < S.size() - 1){
      cout << ", ";
    }
  }
  cout << "]" <<  endl;
}
void print(vector<vector<ll>> S){
  cout << "["; 
  for(ls_int i = 0; i < S.size(); i++){
    cout << "["; 
    for(ls_int j = 0; j < S.at(i).size(); j++){
      cout << S.at(i).at(j);
      if (j < S.at(i).size() - 1){
        cout << ", ";
      } 
    }
    cout << "]";
    if (i < S.size() - 1){
      cout << ", ";
    }
  }
  cout << "]" <<  endl;
}
void print(vector<vector<float>> S){
  cout << "["; 
  for(ls_int i = 0; i < S.size(); i++){
    cout << "["; 
    for(ls_int j = 0; j < S.at(i).size(); j++){
      cout << S.at(i).at(j);
      if (j < S.at(i).size() - 1){
        cout << ", ";
      } 
    }
    cout << "]";
    if (i < S.size() - 1){
      cout << ", ";
    }
  }
  cout << "]" <<  endl;
}
void print(vector<vector<string>> S){
  cout << "["; 
  for(ls_int i = 0; i < S.size(); i++){
    cout << "["; 
    for(ls_int j = 0; j < S.at(i).size(); j++){
      cout << S.at(i).at(j);
      if (j < S.at(i).size() - 1){
        cout << ", ";
      } 
    }
    cout << "]";
    if (i < S.size() - 1){
      cout << ", ";
    }
  }
  cout << "]" <<  endl;
}


// 2, input list
void input(vector<int> &S, int N){
  int a;
  for (int i = 1; i <= N; i++){
    cin >> a;
    S.push_back(a);
  }
}
void input(vector<ll> &S, int N){
  ll a;
  for (int i = 1; i <= N; i++){
    cin >> a;
    S.push_back(a);
  }
}
void input(vector<float> &S, int N){
  float a;
  for (int i = 1; i <= N; i++){
    cin >> a;
    S.push_back(a);
  }
}

// 3, sum of S[l, r)
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
  for (ls_int _ = ls_int(l); _ < ls_int(r); _++){
      ans += S[_];
  }
  return ans;
}

// *** main function ***
int main(){
  cin.tie(nullptr);
  ios_base::sync_with_stdio(false);
  cout << fixed << setprecision(16);
  
  // *** update from here ***
  
  int N, M;
  cin >> N >> M;
  
  
}
